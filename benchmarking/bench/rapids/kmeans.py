from cuml import KMeans
from cuml.cluster import KMeans
from sklearn.metrics import accuracy_score

import numpy as np
from .. import common


args = common.build_argument_parser().parse_args()

print("Fit dataset:", args.fit_file)

dtype = np.float64 if args.double else np.float32
print("Type elements:", dtype)

X, y = common.open_auto_extract_dataset(args.fit_file, dtype)
print("Fit targets:", y.shape)
print("Fit samples:", X.shape)

b = common.np_to_cudf(X)

common.cuda_warm_up()

timer = common.Timer()
model = KMeans(n_clusters=2)
model.fit(b)
print("Fit time:", timer.count())

common.print_params({
    "labels": model.labels_,
    "cluster_centers": model.cluster_centers_,
})

if (args.test):
    print("Test dataset:", args.test_file)
    X_t, y_t = common.open_auto_extract_dataset(args.test_file, dtype)
    print("Test targets:", y_t.shape)
    print("Test samples:", X_t.shape)

    b_t = common.np_to_cudf(X_t)

    timer = common.Timer()
    preds = model.predict(X_t)
    print("Predicting time:", timer.count())

    common.print_params({
        "Real": y_t,
        "Predictions": preds,
    }, space="\n")

    common.print_many("#")
    common.print_params({
        "Predictions score": model.score(X_t),
        "Accuracy score": accuracy_score(y_t, preds),
    })
