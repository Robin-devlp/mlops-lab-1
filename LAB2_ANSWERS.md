Lab 2 Answers


Question 1: Look at pyproject.toml and uv.lock. What changed?

In pyproject.toml the four new libraries were added to the dependencies list with their minimum versions: mlflow 3.16.0, scikit-learn 1.9.1, torch 2.14.0 and torchvision 0.29.0. The pytorch-cpu section I added before running uv add is also there and tells uv to get torch and torchvision from the CPU-only PyTorch index instead of PyPI. uv.lock got much bigger and went from 2 packages to 100, because mlflow and torch bring a lot of other libraries with them. It pins the exact version of every package with its download links and hashes, and torch and torchvision point to the PyTorch CPU index with versions ending in +cpu.


Question 2: What is `--backend-store-uri` used for? What is `--default-artifact-root` used for? What is the difference between the metadata mlflow stores and the artifacts it stores?

--backend-store-uri tells mlflow where to store the tracking metadata. Here it is sqlite:///mlflow.db so it is saved in a SQLite database file in the repo, which has tables for experiments, runs, params, metrics and tags. --default-artifact-root is the folder where each run saves its artifacts, here ./mlruns, and the Default experiment points to mlruns/0. The metadata is the small information about the runs like the params, metrics, tags and run IDs that the UI uses to search and compare runs. The artifacts are the actual files a run produces like the trained model, which are much bigger so they are stored as files in the artifact folder and not in the database.


Question 3: Why shouldn't `mlflow.db` and `mlruns/` be tracked by git, and why shouldn't they be tracked by dvc either?

They are created by running the server and the training and they are not code, so git is not the right place for them. mlflow.db is a binary database that changes every time a run is logged and mlruns will hold the saved models, so they would make the git history heavy and cause conflicts since everyone has their own local runs. DVC is not a good fit either because it is meant for versioning the data that the code uses, not the results of experiments. MLflow already keeps track of every run with its own run IDs, params, metrics and saved models, so tracking these files with DVC would only duplicate that while the database keeps changing as long as the server is running.


Question 4: What happens the first time you call `set_experiment` with a name that doesn't exist yet? Check the mlflow UI.

MLflow checks if an experiment with that name exists and since food11 did not exist it created it automatically and printed that it was creating a new experiment. After refreshing the UI a new experiment called food11 appears next to Default with ID 1 and no runs yet, and its artifacts will be saved in mlruns/1. Calling set_experiment again with the same name does not create a second one and just uses the existing experiment as the active one for the next runs.


Question 5: What is the difference between `mlflow.log_param` and `mlflow.log_metric`? Why does `log_metric` take a `step` argument and `log_param` doesn't?

log_param saves a setting that is chosen before training and stays the same for the whole run, like the learning rate or the batch size, so it is logged once as a single value. log_metric saves a number that comes out of the training and can change over time, like the loss or the accuracy. That is why log_metric takes a step, so each value is saved with the epoch it belongs to and mlflow can draw how it changes during training. In my run train_loss, val_loss and val_accuracy each have 5 values for steps 1 to 5 while lr only has one value, and a param cannot be logged again with a different value in the same run.


Question 6: Open the run in the mlflow UI. Find the params, the metric charts, and the logged model artifact. Where does the model artifact actually live on disk?

On the run page I can see the params like lr 0.001, batch_size 32, epochs 5 and dataset mini, and the metric charts for train_loss, val_loss and val_accuracy over the 5 epochs together with the final test_accuracy. The model is listed as a logged model called model that is linked to the run. It does not live in the run's own artifacts folder, which is empty, but in mlruns/1/models/m-bf4ebc2e363b434a942425ad8a7eecda/artifacts inside the repo. That folder has data/model.pt2 with the trained model which is about 44 MB, the MLmodel file that describes it and the requirements and input example files, while mlflow.db only stores the path to it.
