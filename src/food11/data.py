"""Prepare the Food-11 images for training.

Builds two datasets from data/food11_raw:
- data/food11_processed: every image resized to 128x128 and sorted into one
  folder per category, which is the layout torchvision's ImageFolder expects.
- data/food11_processed_mini: the same, with at most 100 images per category.
"""
import shutil
from pathlib import Path

from PIL import Image, ImageOps

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
SPLITS = ["training", "evaluation", "validation"]
IMAGE_SIZE = (128, 128)
MINI_PER_CATEGORY = 100

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
RAW_DIR = DATA_DIR / "food11_raw"
PROCESSED_DIR = DATA_DIR / "food11_processed"
MINI_DIR = DATA_DIR / "food11_processed_mini"


def sort_key(path):
    # file names look like "<category>_<index>.jpg"
    category, index = path.stem.split("_")
    return int(category), int(index)


def process_split(split):
    counts = [0] * len(CATEGORIES)
    for src in sorted((RAW_DIR / split).glob("*.jpg"), key=sort_key):
        label = sort_key(src)[0]
        category = CATEGORIES[label]

        dst = PROCESSED_DIR / split / category / src.name
        dst.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(src) as img:
            # crop the centre to a square first so non-square images are not stretched
            small = ImageOps.fit(img.convert("RGB"), IMAGE_SIZE, Image.Resampling.LANCZOS)
            small.save(dst, quality=95)

        counts[label] += 1
        if counts[label] <= MINI_PER_CATEGORY:
            mini_dst = MINI_DIR / split / category / src.name
            mini_dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(dst, mini_dst)
    return counts


def main():
    for folder in (PROCESSED_DIR, MINI_DIR):
        if folder.exists():
            shutil.rmtree(folder)

    for split in SPLITS:
        counts = process_split(split)
        print(f"{split}: {sum(counts)} images")
        for name, n in zip(CATEGORIES, counts):
            print(f"  {name:<16} {n:5}  mini: {min(n, MINI_PER_CATEGORY)}")


if __name__ == "__main__":
    main()
