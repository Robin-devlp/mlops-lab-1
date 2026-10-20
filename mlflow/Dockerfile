FROM python:3.11-slim

RUN pip install --no-cache-dir mlflow

EXPOSE 5000

# --serve-artifacts makes the server itself hand out the model files over HTTP,
# and --default-artifact-root mlflow-artifacts:/ makes runs store them through
# that proxy. Without it the runs would point at /mlflow-data/mlruns, a path
# that only exists inside this container, so the inference service could not
# read the model. --artifacts-destination is where the server keeps them, on
# the volume mounted at /mlflow-data.
CMD ["mlflow", "server", \
     "--host", "0.0.0.0", "--port", "5000", \
     "--backend-store-uri", "sqlite:////mlflow-data/mlflow.db", \
     "--serve-artifacts", \
     "--artifacts-destination", "/mlflow-data/mlruns", \
     "--default-artifact-root", "mlflow-artifacts:/"]
