from cuml import PCA
from cuml.decomposition import PCA
from sklearn.metrics import accuracy_score

import numpy as np
from .. import common


args = common.build_argument_parser(test_file=False, test=False).parse_args()

print("Fit dataset:", args.fit_file)

dtype = np.float64 if args.double else np.float32
print("Type elements:", dtype)

X, y = common.open_auto_extract_dataset(args.fit_file, dtype)
print("Fit targets:", y.shape)
print("Fit samples:", X.shape)

b = common.np_to_cudf(X)

common.cuda_warm_up()

timer = common.Timer()
model = PCA(n_components=2)
model.fit(b)
print("Fit time:", timer.count())

trans_gdf_float = model.transform(b)
input_gdf_float = model.inverse_transform(trans_gdf_float)
common.print_params({
    "components": model.components_,
    "explained variance": model.explained_variance_,
    "explained variance ratio": model.explained_variance_ratio_,
    "singular values": model.singular_values_,
    "mean": model.mean_,
    "noise variance": model.noise_variance_,
    "inverse": trans_gdf_float,
    "input": input_gdf_float,
}, space="\n")
