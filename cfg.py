from pathlib import Path

DATA_URL = "https://raw.githubusercontent.com/mlflow/mlflow/master/examples/docker/wine-quality.csv"

_p = Path(__file__).resolve().parent

CSV_PATH = _p / "wine-quality.csv"
OUTPUT_PATH = _p / "outputs"
Path(OUTPUT_PATH).mkdir(exist_ok=True, parents=True)
RANDOM_SEED = 42
