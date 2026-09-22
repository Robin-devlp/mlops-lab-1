***Robin Ghassibeh (231463)***

### Question 1: Open the "Models" tab in the mlflow UI. What version number was your model given? What's the difference between a run's logged model artifact and a registered model?

The model was registered as food11 and got version 1, since it is the first one with that name. A logged model is just the files saved by one training run, like model.pt2. A registered model is a name in the Model Registry that groups versions from different runs, so a better model later would become version 2 without changing version 1.

### Question 2: What aliases replaced the old built-in stages in mlflow? Why version a model separately from the run that produced it, and why is an alias more flexible than a fixed stage name?

The old stages Staging, Production and Archived were replaced by aliases, names we choose ourselves like champion or challenger, plus tags. I gave version 1 the alias champion. Versioning the model apart from the run lets the serving code just ask for food11 without caring which run made it. An alias is more flexible because it can be moved to any version at any time, while stages were a fixed list.

### Question 3: Why load the model through an mlflow model URI (`models:/food11@champion`) instead of pointing directly at the `.pth` file on disk? What would you have to change to serve a newer model version?

With models:/food11@champion the code does not need to know where the model file is, since MLflow finds the version the alias points to and loads it. A file path would tie the code to one machine, and my model is a model.pt2 under a generated ID anyway. To serve a newer version I would register it, move the champion alias to it and restart the service, with no code change.

### Question 4: Why copy `pyproject.toml`/`uv.lock` and run `uv sync` *before* copying the rest of the source code, instead of copying everything at once? What happens to the build cache when you only change a line in `serve.py`?

pyproject.toml and uv.lock rarely change while the code changes all the time, and Docker only reuses a cached layer if that step and all the ones before it are unchanged. When I added one line to serve.py and rebuilt, every step including uv sync was cached and only COPY src/ ran again, so it took 3 seconds instead of 27 minutes. If everything was copied at once, any code change would rerun uv sync.

### Question 5: What's the size difference between a naive single-stage image and your multi-stage one? Use `docker history <image>` to see which layers are the biggest.

My multi-stage image is 1.99 GB and the naive single-stage one is 2.08 GB, about 90 MB more. docker history shows the biggest layer in both is the 1.43 GB virtual environment, mostly torch. The naive image also keeps uv itself, a 60 MB layer, and all the copied files. Without the build cache mount it would also keep uv's 1.4 GB download cache, so about 3.5 GB.

### Question 6: What happens to build speed and image size if you forget the `.dockerignore`? Which of the excluded folders would actually break the build if they were sent to the Docker daemon?

Without it Docker has to send the whole project folder, about 4.1 GB with data, the .dvc cache, .venv and mlruns, instead of 484 kB, so every build starts much slower. My image would stay the same size because the Dockerfile only copies pyproject.toml, uv.lock and src/, but a COPY . . would put all of it inside. The .venv is the one that breaks things, since it is a Windows environment and would replace the Linux one.
