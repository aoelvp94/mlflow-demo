import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def compute_rmse(actual, pred):
    return np.sqrt(mean_squared_error(actual, pred))


def compute_mae(actual, pred):
    return mean_absolute_error(actual, pred)


def compute_r2(actual, pred):
    return r2_score(actual, pred)
