Lab 2 Answers


Question 1: Look at pyproject.toml and uv.lock. What changed?

In pyproject.toml the four new libraries were added to the dependencies list with their minimum versions: mlflow 3.16.0, scikit-learn 1.9.1, torch 2.14.0 and torchvision 0.29.0. The pytorch-cpu section I added before running uv add is also there and tells uv to get torch and torchvision from the CPU-only PyTorch index instead of PyPI. uv.lock got much bigger and went from 2 packages to 100, because mlflow and torch bring a lot of other libraries with them. It pins the exact version of every package with its download links and hashes, and torch and torchvision point to the PyTorch CPU index with versions ending in +cpu.


Question 2: What is `--backend-store-uri` used for? What is `--default-artifact-root` used for? What is the difference between the metadata mlflow stores and the artifacts it stores?

--backend-store-uri tells mlflow where to store the tracking metadata. Here it is sqlite:///mlflow.db so it is saved in a SQLite database file in the repo, which has tables for experiments, runs, params, metrics and tags. --default-artifact-root is the folder where each run saves its artifacts, here ./mlruns, and the Default experiment points to mlruns/0. The metadata is the small information about the runs like the params, metrics, tags and run IDs that the UI uses to search and compare runs. The artifacts are the actual files a run produces like the trained model, which are much bigger so they are stored as files in the artifact folder and not in the database.
