from pathlib import Path
from urllib.request import urlretrieve

import numpy as np


IRIS_URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data"


def one_hot(y: np.ndarray, num_classes: int) -> np.ndarray:
    encoded = np.zeros((y.size, num_classes), dtype=np.float64)
    encoded[np.arange(y.size), y] = 1.0
    return encoded


def train_test_split(X: np.ndarray, y: np.ndarray, test_ratio: float = 0.2, seed: int = 42):
    rng = np.random.default_rng(seed)
    indices = np.arange(X.shape[0])
    rng.shuffle(indices)

    test_size = int(X.shape[0] * test_ratio)
    test_idx = indices[:test_size]
    train_idx = indices[test_size:]

    return X[train_idx], X[test_idx], y[train_idx], y[test_idx]


def standardize_fit(X: np.ndarray):
    mean = X.mean(axis=0, keepdims=True)
    std = X.std(axis=0, keepdims=True)
    std[std == 0] = 1.0
    return mean, std


def standardize_transform(X: np.ndarray, mean: np.ndarray, std: np.ndarray):
    return (X - mean) / std


def download_iris_if_needed(data_path: Path):
    if data_path.exists():
        return
    data_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"Downloading Iris dataset to {data_path}...")
    urlretrieve(IRIS_URL, data_path)


def load_dataset(
    data_path: Path,
    delimiter: str = ",",
    target_col: int = -1,
    has_header: bool = False,
):
    skip_header = 1 if has_header else 0
    data = np.genfromtxt(
        data_path,
        delimiter=delimiter,
        dtype=str,
        skip_header=skip_header,
    )

    if data.ndim == 1:
        data = data.reshape(1, -1)

    data = data[np.any(data != "", axis=1)]

    if target_col < 0:
        target_col = data.shape[1] + target_col

    y_raw = data[:, target_col]
    X_raw = np.delete(data, target_col, axis=1)

    X = X_raw.astype(np.float64)
    classes, y = np.unique(y_raw, return_inverse=True)

    return X, y.astype(np.int64), classes


def prepare_data(
    data_path: Path,
    delimiter: str = ",",
    target_col: int = -1,
    has_header: bool = False,
    seed: int = 42,
    test_ratio: float = 0.2,
):
    if not data_path.exists() and "iris" in data_path.name.lower():
        download_iris_if_needed(data_path)

    if not data_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at {data_path}. Provide a CSV with numeric features and class label column."
        )

    X, y, classes = load_dataset(
        data_path=data_path,
        delimiter=delimiter,
        target_col=target_col,
        has_header=has_header,
    )

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_ratio=test_ratio, seed=seed)

    mean, std = standardize_fit(X_train)
    X_train = standardize_transform(X_train, mean, std)
    X_test = standardize_transform(X_test, mean, std)

    return X_train, X_test, y_train, y_test, classes
