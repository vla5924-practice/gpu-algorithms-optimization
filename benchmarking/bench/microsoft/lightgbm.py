import lightgbm
import numpy as np

from sklearn.metrics import accuracy_score

from ..common import argparser, dataset, utils
# from ..common import cuda
from ..common.timer import Timer


args = argparser.build_parser().parse_args()

print("Fit dataset:", args.fit_file)

dtype = np.float64 if args.double else np.float32
print("Type elements:", dtype)

X, y = dataset.open_auto_extract_dataset(args.fit_file, dtype)
print("Fit targets:", y.shape)
print("Fit samples:", X.shape)

# common.cuda_warm_up()

timer = Timer()
params = {
    "objective": "binary",
    "metric": "auc",
    "device": "cpu",
    # "device": "gpu",
    # "gpu_device_id": 0,
}
model = lightgbm.LGBMClassifier(**params)
model.fit(X, y)
print("Fit time:", timer.count())

if (args.test):
    if args.test_file:
        print("Test dataset:", args.test_file)
        X_t, y_t = dataset.open_auto_extract_dataset(args.test_file, dtype)
    else:
        print("Test dataset:", args.fit_file)
        X_t, y_t = X, y
    print("Test targets:", y_t.shape)
    print("Test samples:", X_t.shape)

    timer = Timer()
    preds = model.predict(X_t)
    print("Predicting time:", timer.count())

    utils.print_params({
        "Real": y_t,
        "Predictions": preds,
    }, space="\n")

    utils.print_many("#")
    utils.print_params({
        "Accuracy score": accuracy_score(y_t, preds),
    })
