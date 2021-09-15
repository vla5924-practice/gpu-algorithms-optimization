import lightgbm
import numpy as np

from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.model_selection import train_test_split

from ..common import argparser, cuda, dataset, utils
from ..common.timer import Timer


args = argparser.build_parser().parse_args()

print("Fit dataset:", args.fit_file)

dtype = np.float64 if args.double else np.float32
print("Type elements:", dtype)

X, y = dataset.open_auto_extract_dataset(args.fit_file, dtype)
print("Fit targets:", y.shape)
print("Fit samples:", X.shape)

if 0 < args.fit_size < 1:
    X, X_t, y, y_t = train_test_split(
        X, y, train_size=args.fit_size, random_state=5924)
utils.print_metric("Fit size", "FSZ", args.fit_size)

cuda.cuda_warm_up()

timer = Timer()
params = {
    "objective": "binary",
    "metric": "auc",
    "device": "cuda",
    "verbosity": 1,
    # "device": "gpu",
    # "gpu_device_id": 0,
}
model = lightgbm.LGBMClassifier(**params)
model.fit(X, y)
utils.print_metric("Fit time", "FIT", timer.count())

if (args.test):
    if args.test_file:
        print("Test dataset:", args.test_file)
        X_t, y_t = dataset.open_auto_extract_dataset(args.test_file, dtype)
    elif args.fit_size == 1:
        print("Test dataset:", args.fit_file)
        X_t, y_t = X, y
    else:
        print("Test dataset is {} portion of fit dataset".format(1 - args.fit_size))
    print("Test targets:", y_t.shape)
    print("Test samples:", X_t.shape)

    timer = Timer()
    preds = model.predict(X_t)
    utils.print_metric("Predicting time", "PRD", timer.count())

    utils.print_metric("Accuracy score", "ACC", accuracy_score(y_t, preds))
    utils.print_metric("Mean-squared error", "MSE", mean_squared_error(y_t, preds))
