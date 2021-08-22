from argparse import ArgumentParser

import arff
import cudf
import numpy as np
import os
import pandas as pd
import time


def build_argument_parser(fit_file=True, fit_size=True, test_file=True, test=True, double=True) -> ArgumentParser:
    parser = ArgumentParser()
    if fit_file:
        parser.add_argument("-ff", "--fit_file", dest="fit_file",
                            help="dataset file for fit", metavar="FILE")
    if fit_size:
        parser.add_argument("-s", "--fit_size", type=float, default=1,
                            help="portion of dataset to split and fit on (between 0 and 1)", metavar="FLOAT")
    if test_file:
        parser.add_argument("-tf", "--test_file", dest="test_file",
                            help="dataset file for test", metavar="FILE")
    if test:
        parser.add_argument("--test", action="store_true")
    if double:
        parser.add_argument("--double", action="store_true")
    return parser


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


def cuda_warm_up() -> None:
    from cuml.linear_model import LogisticRegression
    X = cudf.DataFrame()
    X["col1"] = np.array([1, 1, 2, 2], dtype=np.float32)
    X["col2"] = np.array([1, 2, 2, 3], dtype=np.float32)
    y = cudf.Series(np.array([0.0, 0.0, 1.0, 1.0], dtype=np.float32))
    model = LogisticRegression()
    model.fit(X, y)


def np_to_cudf(df: np.ndarray):
    df = pd.DataFrame({"fea%d" % i: df[:, i] for i in range(df.shape[1])})
    pdf = cudf.DataFrame()
    for c, column in enumerate(df):
        pdf[str(c)] = df[column]
    return pdf


def print_many(symbol: str, n=40) -> None:
    print(symbol * n)


def print_params(params: dict, space=" ") -> None:
    for key in params:
        print("{}:{}{}".format(key, space, params[key]))


class Timer:
    def __init__(self):
        self.reset()

    def reset(self):
        self._timer = time.perf_counter()

    def count(self):
        current = time.perf_counter()
        return current - self._timer
