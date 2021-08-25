import arff
import numpy as np
import os


def open_arff(filename: str) -> np.ndarray:
    arff_data = arff.load(open(filename, "r"))
    data = np.array(arff_data["data"])
    return data


def extract_dataset(data: np.ndarray, type) -> tuple:
    y = data[:, 0]
    y = y.astype(int)
    X = np.delete(data, 0, 1)
    X = np.array(X, dtype=type)
    return (X, y)


def open_npy_extract_dataset(filename: str, type) -> tuple:
    with open(filename, "rb") as f:
        y = np.load(f)
        X = np.load(f)
    return (X, y)


def open_auto_extract_dataset(filename: str, type) -> tuple:
    file_ext = os.path.splitext(filename)[1]
    if file_ext == ".arff":
        fit_data = open_arff(filename)
        return extract_dataset(fit_data, type)
    elif file_ext in [".npy", ".bin"]:
        return open_npy_extract_dataset(filename, type)
    else:
        raise ValueError(
            "Unsupported file format. Only arff and npy are supported.")
