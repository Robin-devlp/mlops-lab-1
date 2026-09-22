"""Serve the champion Food-11 model with FastAPI.

Run locally from the repo root:
    uv run uvicorn src.food11.serve:app --host 0.0.0.0 --port 8000
"""
import io
import os
from contextlib import asynccontextmanager

import mlflow
import numpy as np
from fastapi import FastAPI, File, HTTPException, UploadFile
from PIL import Image, ImageOps, UnidentifiedImageError

MODEL_URI = "models:/food11@champion"
TRACKING_URI = os.environ.get("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")

# same order as the class indices ImageFolder gave the category folders in training
CATEGORIES = [
    "Bread",
    "Dairy product",
    "Dessert",
    "Egg",
    "Fried food",
    "Meat",
    "Noodles-Pasta",
    "Rice",
    "Seafood",
    "Soup",
    "Vegetable-Fruit",
]
IMAGE_SIZE = (128, 128)
# the ImageNet statistics train.py normalised the images with
MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)


@asynccontextmanager
async def lifespan(app):
    # load the model once at startup instead of on every request
    mlflow.set_tracking_uri(TRACKING_URI)
    app.state.model = mlflow.pyfunc.load_model(MODEL_URI)
    yield


app = FastAPI(title="Food-11 classifier", lifespan=lifespan)


def preprocess(data):
    image = Image.open(io.BytesIO(data)).convert("RGB")
    # training used 128x128 centre crops, so other sizes get the same treatment
    image = ImageOps.fit(image, IMAGE_SIZE, Image.Resampling.LANCZOS)
    array = (np.asarray(image, dtype=np.float32) / 255.0 - MEAN) / STD
    # height x width x channels -> a batch of one channels x height x width image
    return array.transpose(2, 0, 1)[np.newaxis]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(file: UploadFile = File(...)):
    try:
        batch = preprocess(file.file.read())
    except UnidentifiedImageError:
        raise HTTPException(status_code=400, detail="The uploaded file is not an image")
    logits = np.asarray(app.state.model.predict(batch))[0]
    # softmax turns the 11 raw scores into probabilities that add up to 1
    probs = np.exp(logits - logits.max())
    probs /= probs.sum()
    best = int(probs.argmax())
    return {"category": CATEGORIES[best], "confidence": round(float(probs[best]), 4)}
