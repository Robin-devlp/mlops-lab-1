"""Train a ResNet18 on Food-11 and track the run with MLflow.

Example:
    uv run python ./src/food11/train.py --dataset mini --epochs 5 --lr 0.001 --batch-size 32
"""
import argparse
from pathlib import Path

import mlflow
import mlflow.pytorch
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
from torchvision.models import ResNet18_Weights, resnet18

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
DATASETS = {
    "processed": DATA_DIR / "food11_processed",
    "mini": DATA_DIR / "food11_processed_mini",
}

# the images are already 128x128, so they only need to be normalised with the
# ImageNet statistics the pretrained weights were trained with
TRANSFORM = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])


def parse_args():
    parser = argparse.ArgumentParser(description="Train ResNet18 on Food-11")
    parser.add_argument("--dataset", choices=DATASETS, default="mini")
    parser.add_argument("--epochs", type=int, default=5)
    parser.add_argument("--lr", type=float, default=0.001)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--seed", type=int, default=42)
    return parser.parse_args()


def make_loader(root, split, batch_size, shuffle):
    dataset = datasets.ImageFolder(root / split, transform=TRANSFORM)
    return DataLoader(dataset, batch_size=batch_size, shuffle=shuffle)


def build_model(num_classes):
    model = resnet18(weights=ResNet18_Weights.DEFAULT)
    # replace the 1000-class ImageNet head with one for the food categories
    model.fc = nn.Linear(model.fc.in_features, num_classes)
    return model


def train_one_epoch(model, loader, criterion, optimizer, device):
    model.train()
    total_loss = 0.0
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        loss = criterion(model(images), labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * labels.size(0)
    return total_loss / len(loader.dataset)


@torch.no_grad()
def evaluate(model, loader, criterion, device):
    model.eval()
    total_loss, correct = 0.0, 0
    for images, labels in loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        total_loss += criterion(outputs, labels).item() * labels.size(0)
        correct += (outputs.argmax(dim=1) == labels).sum().item()
    n = len(loader.dataset)
    return total_loss / n, correct / n


def main():
    args = parse_args()
    torch.manual_seed(args.seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    root = DATASETS[args.dataset]
    train_loader = make_loader(root, "training", args.batch_size, shuffle=True)
    val_loader = make_loader(root, "validation", args.batch_size, shuffle=False)
    test_loader = make_loader(root, "evaluation", args.batch_size, shuffle=False)
    classes = train_loader.dataset.classes
    assert classes == val_loader.dataset.classes == test_loader.dataset.classes

    model = build_model(len(classes)).to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=args.lr)

    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    mlflow.set_experiment("food11")

    with mlflow.start_run() as run:
        mlflow.log_params({
            "dataset": args.dataset,
            "epochs": args.epochs,
            "lr": args.lr,
            "batch_size": args.batch_size,
            "seed": args.seed,
            "model": "resnet18",
            "optimizer": "adam",
        })

        for epoch in range(1, args.epochs + 1):
            train_loss = train_one_epoch(model, train_loader, criterion, optimizer, device)
            val_loss, val_accuracy = evaluate(model, val_loader, criterion, device)
            mlflow.log_metric("train_loss", train_loss, step=epoch)
            mlflow.log_metric("val_loss", val_loss, step=epoch)
            mlflow.log_metric("val_accuracy", val_accuracy, step=epoch)
            print(f"epoch {epoch}/{args.epochs}  train_loss {train_loss:.4f}  "
                  f"val_loss {val_loss:.4f}  val_accuracy {val_accuracy:.4f}")

        _, test_accuracy = evaluate(model, test_loader, criterion, device)
        mlflow.log_metric("test_accuracy", test_accuracy)
        print(f"test_accuracy {test_accuracy:.4f}")

        # MLflow 3 renamed log_model's second argument to name, and its default "pt2"
        # format needs an example batch to trace the model. More than one image keeps
        # the batch size flexible for later predictions.
        example_images, _ = next(iter(test_loader))
        mlflow.pytorch.log_model(model.cpu(), name="model", input_example=example_images[:2].numpy())
        print(f"run_id {run.info.run_id}")


if __name__ == "__main__":
    main()
