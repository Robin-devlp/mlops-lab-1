***Robin Ghassibeh (231463)***


### Question 1: Open the "Models" tab in the mlflow UI. What version number was your model given? What's the difference between a run's logged model artifact and a registered model?

The model was registered as food11 and got version 1, since it is the first version with that name. The logged model artifact is just the files saved by one training run, like model.pt2 and the MLmodel file. A registered model is a name in the Model Registry that groups versions coming from different runs, each one linking back to its run. Version 1 points to my best run zealous-turtle-10, and a better model later would become version 2 without changing version 1.


### Question 2: What aliases replaced the old built-in stages in mlflow? Why version a model separately from the run that produced it, and why is an alias more flexible than a fixed stage name?

The old stages Staging, Production and Archived were replaced by aliases, which are names we choose ourselves like champion for the model in use and challenger for one being tested, plus tags for extra information. I gave version 1 of food11 the alias champion. Versioning the model separately from the run lets the serving code just ask for food11 without caring which run produced it, while each version still links back to its run. An alias is more flexible because it is a pointer that can be moved to another version at any time and one version can have several aliases, while stages were a fixed list and a version could only be in one of them.


### Question 3: Why load the model through an mlflow model URI (`models:/food11@champion`) instead of pointing directly at the `.pth` file on disk? What would you have to change to serve a newer model version?

With models:/food11@champion the code does not need to know where the model file is or which run it came from, since MLflow finds the version the champion alias points to and loads it. Pointing at a file would tie the code to one path on one machine, and my model is not even a .pth file but a model.pt2 under a generated ID in mlruns. To serve a newer version I would register it as version 2, move the champion alias to it and restart the service, without changing the code or the Docker image.
