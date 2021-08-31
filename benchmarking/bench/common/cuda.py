import cudf
import numpy as np
import pandas as pd


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
