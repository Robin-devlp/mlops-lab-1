***Robin Ghassibeh (231463)***

### Question 1: Why is it a bad idea for a unit test to load the real model from your MLflow server? List at least two ways the test could fail even though your code is correct.

A unit test should only check my own code, quickly and the same way every time, and loading the real model ties it to things outside the code. If the MLflow server is down, like on a CI runner that cannot reach my laptop, the test fails after minutes of retries. If someone moves the champion alias, the predictions change and the assertions break even though nothing in my code changed.
