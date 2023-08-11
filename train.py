# The data set used in this example is from http://archive.ics.uci.edu/ml/datasets/Wine+Quality
# P. Cortez, A. Cerdeira, F. Almeida, T. Matos and J. Reis.
# Modeling wine preferences by data mining from physicochemical properties. In Decision Support Systems, Elsevier, 47(4):547-553, 2009.

import argparse
from datetime import datetime
import os

import mlflow
import numpy as np
import pandas as pd
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import train_test_split

import cfg
import metrics
from plotter import plot_normalized_distplot

if __name__ == "__main__":

    np.random.seed(cfg.RANDOM_SEED)
    MLFLOW_ARTIFACT_ROOT = os.environ['MLFLOW_ARTIFACT_ROOT']
    MLFLOW_TRACKING_USERNAME = os.environ['MLFLOW_TRACKING_USERNAME']
    MLFLOW_TRACKING_PASSWORD = os.environ['MLFLOW_TRACKING_PASSWORD']
    MLFLOW_SERVER_HOST = os.environ['MLFLOW_SERVER_HOST']
    MLFLOW_SERVER_PORT = os.environ['MLFLOW_SERVER_PORT']

    parser = argparse.ArgumentParser()
    parser.add_argument("--alpha")
    parser.add_argument("--l1-ratio")
    args = parser.parse_args()
    # Read the wine-quality csv file (make sure you're running this from the root of MLflow!)
    data = pd.read_csv(cfg.DATA_URL)
    # Split the data into training and test sets. (0.75, 0.25) split.
    train, test = train_test_split(data)

    # The predicted column is "quality" which is a scalar from [3, 9]
    train_x = train.drop(["quality"], axis=1)
    test_x = test.drop(["quality"], axis=1)
    train_y = train[["quality"]]
    test_y = test[["quality"]]

    alpha = float(args.alpha)
    l1_ratio = float(args.l1_ratio)
    model_name = "ElasticNet"
    experiment_name = f"wine_{model_name}"
    execution_date = datetime.today().strftime("%Y%m%d")

    run_name = f"{experiment_name}_{execution_date}"
    try:
        mlflow.create_experiment(  # pylint: disable=no-member
            experiment_name, MLFLOW_ARTIFACT_ROOT
        )
    except Exception as exc:
        if str(exc) == f"Experiment '{experiment_name}' already exists.":
            pass
        else:
            raise exc
    
    mlflow.set_tracking_uri(f'http://{MLFLOW_TRACKING_USERNAME}:{MLFLOW_TRACKING_PASSWORD}@{MLFLOW_SERVER_HOST}:{MLFLOW_SERVER_PORT}')
    mlflow.set_experiment(experiment_name)
    with mlflow.start_run(run_name=run_name) as run:
        lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=cfg.RANDOM_SEED)
        lr.fit(train_x, train_y)

        predicted_qualities = lr.predict(test_x)

        rmse = metrics.compute_rmse(test_y, predicted_qualities)
        mae = metrics.compute_mae(test_y, predicted_qualities)
        r2 = metrics.compute_r2(test_y, predicted_qualities)

        print("Elasticnet model (alpha=%f, l1_ratio=%f):" % (alpha, l1_ratio))
        print("  RMSE: %s" % rmse)
        print("  MAE: %s" % mae)
        print("  R2: %s" % r2)

        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)
        mlflow.sklearn.log_model(lr, "model")
        # Create and save simple plot
        params = {"xlabel": "Predicted Quality", "title": "Prediction Distribution"}
        CODE_PATH = cfg.OUTPUT_PATH / "code"
        plot_normalized_distplot(
            predicted_qualities,
            save_path=CODE_PATH / "pred_displot.png",
            **params
        )
        # Upload all contents of ./outputs to tracking server
        mlflow.log_artifacts(CODE_PATH, artifact_path="artifacts")
