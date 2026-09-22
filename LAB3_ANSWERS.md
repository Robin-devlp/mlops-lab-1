Lab 3 Answers


Question 1: Open the "Models" tab in the mlflow UI. What version number was your model given? What's the difference between a run's logged model artifact and a registered model?

The model was registered under the name food11 and got version 1, since it is the first version with that name. The logged model artifact is just the files saved by one training run, like model.pt2 and the MLmodel file, and it only belongs to that run. A registered model is a name in the Model Registry that groups versions of a model coming from different runs, and each version points back to the run it came from. Here version 1 points to the model of my best run zealous-turtle-10, and a better model from another run would become version 2 under the same name without changing version 1.


Question 2: What aliases replaced the old built-in stages in mlflow? Why version a model separately from the run that produced it, and why is an alias more flexible than a fixed stage name?

The old stages Staging, Production and Archived were replaced by aliases, which are names we choose ourselves like champion for the model in use and challenger for a new one being tested, plus tags for any extra information. I gave version 1 of food11 the alias champion. Versioning the model separately from the run gives it its own history under one name, so the serving code can ask for food11 without caring which training run or experiment it came from, while each version still links back to its run. An alias is more flexible because it is just a pointer that can be moved to another version at any time without changing the version numbers, and one version can have several aliases, while the stages were a fixed list and a version could only be in one of them.


Question 3: Why load the model through an mlflow model URI (`models:/food11@champion`) instead of pointing directly at the `.pth` file on disk? What would you have to change to serve a newer model version?

With models:/food11@champion the serving code does not need to know where the model file is or which run it came from, MLflow looks up which version the champion alias points to and loads that model. Pointing at a file would tie the code to one path on one machine, and in my case the model is not even a .pth file but a model.pt2 saved in the mlruns folder under a generated ID. To serve a newer version I would only register the new model as version 2 and move the champion alias to it, then restart the service so it loads the model again. The code and the Docker image would not need to change.
