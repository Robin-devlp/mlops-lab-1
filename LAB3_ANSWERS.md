***Robin Ghassibeh (231463)***


### Question 1: Open the "Models" tab in the mlflow UI. What version number was your model given? What's the difference between a run's logged model artifact and a registered model?

The model was registered as food11 and got version 1, since it is the first one with that name. A logged model is just the files saved by one training run, like model.pt2. A registered model is a name in the Model Registry that groups versions from different runs, so a better model later would become version 2 without changing version 1.


### Question 2: What aliases replaced the old built-in stages in mlflow? Why version a model separately from the run that produced it, and why is an alias more flexible than a fixed stage name?

The old stages Staging, Production and Archived were replaced by aliases, names we choose ourselves like champion or challenger, plus tags. I gave version 1 the alias champion. Versioning the model apart from the run lets the serving code just ask for food11 without caring which run made it. An alias is more flexible because it can be moved to any version at any time, while stages were a fixed list.


### Question 3: Why load the model through an mlflow model URI (`models:/food11@champion`) instead of pointing directly at the `.pth` file on disk? What would you have to change to serve a newer model version?

With models:/food11@champion the code does not need to know where the model file is, since MLflow finds the version the alias points to and loads it. A file path would tie the code to one machine, and my model is a model.pt2 under a generated ID anyway. To serve a newer version I would register it, move the champion alias to it and restart the service, with no code change.
