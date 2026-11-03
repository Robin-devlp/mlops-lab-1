***Robin Ghassibeh (231463)***

### Question 1: Why is it a bad idea for a unit test to load the real model from your MLflow server? List at least two ways the test could fail even though your code is correct.

A unit test should only check my own code, quickly and the same way every time, and loading the real model ties it to things outside the code. If the MLflow server is down, like on a CI runner that cannot reach my laptop, the test fails after minutes of retries. If someone moves the champion alias, the predictions change and the assertions break even though nothing in my code changed.

### Question 2: The fake model always answers "Bread" with 0.90 confidence. What exactly does `test_predict_returns_valid_json` prove, and what does it *not* prove?

It proves the code around the model works: the endpoint accepts an upload, decodes the JPEG, maps the top score to the right class name and returns JSON with a confidence between 0 and 1. It does not prove the real model loads from MLflow or predicts well. My serve.py applies a softmax, so the fake 0.90 came back as 0.1958, and the test still passed since it only checks the range.

![the five unit tests passing in about a second, with the fake model instead of MLflow](images/lab5-q2-pytest.png)
