# MLFLOW V2 - How to run the wine Project?

This directory contains an MLflow project that trains a linear regression model on the UC Irvine Wine Quality Dataset.
The project uses a Docker image to capture the dependencies needed to run training code. Running a project in a Docker
 environment (as opposed to Conda) allows for capturing non-Python dependencies, e.g. Java libraries. 

Steps to reproduce the example:
1. Put a .env file:
```
POSTGRES_HOST=postgres-db
POSTGRES_PORT=6667
POSTGRES_USER=wine
POSTGRES_PASSWORD=wine
IP_SUBNET=189.230.0.0
MLFLOW_POSTGRES_DB=mlflowdb
MLFLOW_ARTIFACT_ROOT=./mlflow/resources/
MLFLOW_TRACKING_USER=mlflow
MLFLOW_TRACKING_PASSWORD=mlflow
MLFLOW_SERVER_HOST=mlflow-server
MLFLOW_UI_HOST=mlflow-ui
MLFLOW_UI_PORT=89
MLFLOW_SERVER_PORT=6001
JUPYTER_PORT=8877
```

2. Build the image:
```bash
docker-compose build
```

3. Setup the project containers
```bash
docker-compose up
```

Check the status of each container with `docker ps` command.


4. In order to execute a run for the specified experiment in `train.py` run:
```bash
docker exec -it base_v2 poetry run python train.py --alpha=2 --l1-ratio=0.2
```
You can try other values for `alpha` and `l1-ratio` parameters to interact with MLFlow service.

5. Go to http://localhost:88/ to see your new experiment and your runs.
   