from argparse import ArgumentParser
from sklearn.datasets import load_svmlight_file
import numpy as np
import os

parser = ArgumentParser()
parser.add_argument("-f", "--file",
                    help="path to svm/svmlight dataset file", metavar="FILE")
parser.add_argument("--double", action="store_true")
args = parser.parse_args()

dtype = np.float64 if args.double else np.float32

print("Dataset file name (arff):", args.file)

svm_data = load_svmlight_file(args.file, dtype=dtype)

y = svm_data[1]
y = np.where(y == -1, 0, y)
y = y - np.min(y, axis=0)
y = y.astype(int)
print("Targets:", y.shape)

X = svm_data[0]
X = X.toarray()
X = np.array(X, dtype=dtype)
print("Samples:", X.shape)

file_npy = os.path.splitext(args.file)[0] + ".npy"
print("Dataset file name (npy):", file_npy)

with open(file_npy, "wb") as f:
    np.save(f, y)
    np.save(f, X)

print("Dataset converted")
