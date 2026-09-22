Lab 3 Answers


Question 1: Open the "Models" tab in the mlflow UI. What version number was your model given? What's the difference between a run's logged model artifact and a registered model?

The model was registered under the name food11 and got version 1, since it is the first version with that name. The logged model artifact is just the files saved by one training run, like model.pt2 and the MLmodel file, and it only belongs to that run. A registered model is a name in the Model Registry that groups versions of a model coming from different runs, and each version points back to the run it came from. Here version 1 points to the model of my best run zealous-turtle-10, and a better model from another run would become version 2 under the same name without changing version 1.
