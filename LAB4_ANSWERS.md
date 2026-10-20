***Robin Ghassibeh (231463)***

### Question 1: What happens to everything written to `/mlflow-data` if you never mount a volume there and just `docker run` this image standalone? Try it: run the container, register nothing, stop it, remove it, start a new one from the same image — what do you see in the UI?

Everything written to /mlflow-data goes into the container's own writable layer, which is deleted together with the container. I created an experiment called q1-volume-demo, then stopped and removed the container and started a new one from the same image. The UI then shows only Default, the experiment is gone and mlflow.db is a brand new empty database.

![before: the UI of the first container, with the q1-volume-demo experiment I created](lab4-q1-before.png)

![after: a new container from the same image, where only Default is left](lab4-q1-after.png)

### Question 2: Why a named volume here instead of a bind mount to a folder in your repo (the way you might for local dev)? Would a bind mount work just as well?

A named volume is managed by Docker itself, so it works the same on any machine without depending on a path inside my repo. A bind mount would also keep the data, but it would drop mlflow's database and artifacts into my project folder where git and dvc would pick them up, and SQLite on a Windows bind mount can hit file locking problems.
