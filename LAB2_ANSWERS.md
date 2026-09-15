Lab 2 Answers


Question 1: Look at pyproject.toml and uv.lock. What changed?

In pyproject.toml the four new libraries were added to the dependencies list with their minimum versions: mlflow 3.16.0, scikit-learn 1.9.1, torch 2.14.0 and torchvision 0.29.0. The pytorch-cpu section I added before running uv add is also there and tells uv to get torch and torchvision from the CPU-only PyTorch index instead of PyPI. uv.lock got much bigger and went from 2 packages to 100, because mlflow and torch bring a lot of other libraries with them. It pins the exact version of every package with its download links and hashes, and torch and torchvision point to the PyTorch CPU index with versions ending in +cpu.
