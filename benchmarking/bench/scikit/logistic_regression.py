import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

from ..common import argparser, cuda, dataset, utils
from ..common.timer import Timer


args = argparser.build_parser().parse_args()

print("Fit dataset:", args.fit_file)

dtype = np.float64 if args.double else np.float32
print("Type elements:", dtype)

X, y = dataset.open_auto_extract_dataset(args.fit_file, dtype)
print("Fit targets:", y.shape)
print("Fit samples:", X.shape)

timer = Timer()
model = LogisticRegression()
model.fit(X, y)
print("Fit time:", timer.count())

utils.print_params({
    "Intercept": model.intercept_,
})

if (args.test):
    print("Test dataset:", args.test_file)
    X_t, y_t = dataset.open_auto_extract_dataset(args.test_file, dtype)
    print("Test targets:", y_t.shape)
    print("Test samples:", X_t.shape)

    b_t = cuda.np_to_cudf(X_t)

    timer = Timer()
    preds = model.predict(X_t)
    print("Predicting time:", timer.count())

    utils.print_params({
        "Real": y_t,
        "Predictions": preds,
    }, space="\n")

    utils.print_many("#")
    utils.print_params({
        "Predictions score": model.decision_function(X_t),
        "Accuracy score": accuracy_score(y_t, preds),
    })
