"""Check a processed Food-11 dataset against its data contract.

Usage:
    uv run python src/food11/validate_data.py data/food11_processed_mini
"""
import argparse
import hashlib
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

from PIL import Image

# the contract states the expected classes itself instead of importing them from
# data.py, so a change in data.py cannot silently change what the check expects
CLASSES = [
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
SPLITS = ["training", "validation", "evaluation"]
SIZE = (128, 128)


def list_images(root):
    """{split: {class: [paths]}} for every class folder that exists."""
    images = {}
    for split in SPLITS:
        folder = root / split
        classes = sorted(p for p in folder.iterdir() if p.is_dir()) if folder.is_dir() else []
        images[split] = {c.name: sorted(c.glob("*.jpg")) for c in classes}
    return images


def check_class_folders(images):
    wrong = [f"{split} has {len(found)}" for split, found in images.items()
             if sorted(found) != sorted(CLASSES)]
    return not wrong, "; ".join(wrong) or f"all {len(SPLITS)} splits have the {len(CLASSES)} class folders"


def check_images(images):
    total, bad = 0, []
    for split in images.values():
        for paths in split.values():
            for path in paths:
                total += 1
                try:
                    with Image.open(path) as img:
                        if img.mode != "RGB" or img.size != SIZE:
                            bad.append(f"{path.name} is {img.mode} {img.size[0]}x{img.size[1]}")
                except OSError:
                    bad.append(f"{path.name} does not open")
    detail = f"{len(bad)} bad, e.g. {bad[0]}" if bad else f"{total} images open, all RGB 128x128"
    return not bad, detail


def check_min_per_class(images, minimum):
    counts = {(split, name): len(paths) for split, found in images.items() for name, paths in found.items()}
    (split, name), smallest = min(counts.items(), key=lambda item: item[1])
    return smallest >= minimum, f"smallest is {name} in {split} with {smallest} (min {minimum})"


def check_no_leakage(images):
    splits_of = defaultdict(set)
    for split, found in images.items():
        for paths in found.values():
            for path in paths:
                splits_of[hashlib.md5(path.read_bytes()).hexdigest()].add(split)
    pairs = Counter()
    for splits in splits_of.values():
        for pair in combinations(sorted(splits), 2):
            pairs["/".join(pair)] += 1
    if not pairs:
        return True, "no image appears in two splits"
    listed = ", ".join(f"{pair} {n}" for pair, n in sorted(pairs.items()))
    return False, f"{sum(pairs.values())} images shared between splits ({listed})"


def check_balance(images, tau):
    train = {name: len(paths) for name, paths in images["training"].items()}
    val = {name: len(paths) for name, paths in images["validation"].items()}
    gaps = {name: abs(train.get(name, 0) / sum(train.values()) - val.get(name, 0) / sum(val.values()))
            for name in CLASSES}
    worst = max(gaps, key=gaps.get)
    return gaps[worst] <= tau, f"largest train/validation share gap is {gaps[worst]:.3f} for {worst} (tau {tau})"


def main():
    parser = argparse.ArgumentParser(description="Validate a processed Food-11 dataset")
    parser.add_argument("dataset", type=Path)
    parser.add_argument("--min-per-class", type=int, default=50)
    parser.add_argument("--tau", type=float, default=0.05)
    args = parser.parse_args()

    images = list_images(args.dataset)
    results = [
        ("class folders", check_class_folders(images)),
        ("images", check_images(images)),
        ("images per class", check_min_per_class(images, args.min_per_class)),
        ("no leakage", check_no_leakage(images)),
        ("class balance", check_balance(images, args.tau)),
    ]

    print(f"data contract for {args.dataset}")
    for number, (name, (passed, detail)) in enumerate(results, start=1):
        print(f"{'PASS' if passed else 'FAIL'}  {number}. {name:<17} {detail}")
    failed = sum(not passed for _, (passed, _) in results)
    print(f"{failed} check(s) failed" if failed else "all checks passed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
