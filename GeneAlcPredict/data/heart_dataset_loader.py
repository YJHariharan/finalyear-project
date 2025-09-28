import os
import pandas as pd


def load_uci_heart_dataset(csv_path: str = os.path.join("data", "heart_uci.csv")):
    """
    Load the UCI Cleveland Heart Disease dataset from a CSV.

    Returns a pandas DataFrame or raises FileNotFoundError if missing.
    Columns typically include: age, sex, cp, trestbps, chol, fbs, restecg,
    thalach, exang, oldpeak, slope, ca, thal, target.
    """
    if not os.path.isfile(csv_path):
        raise FileNotFoundError(f"Dataset not found at {csv_path}")
    df = pd.read_csv(csv_path)
    return df