import numpy as np

from cuml.cluster import KMeans
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

b = cuda.np_to_cudf(X)

cuda.cuda_warm_up()

timer = Timer()
model = KMeans(n_clusters=2)
model.fit(b)
utils.print_metric("Fit time", "FIT", timer.count())

utils.print_metric("Inertia", "INR", model.inertia_)
