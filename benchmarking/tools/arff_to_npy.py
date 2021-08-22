from argparse import ArgumentParser
import os
import arff
import numpy as np


parser = ArgumentParser()
parser.add_argument("-f", "--file",
                    help="path to arff dataset file", metavar="FILE")
parser.add_argument("--double", action="store_true")
args = parser.parse_args()

dtype = np.float64 if args.double else np.float32

print("Dataset file name (arff):", args.file)

arff_data = arff.load(open(args.file, "r"))
data = np.array(arff_data["data"])

y = data[:, 0]
y = y.astype(dtype=dtype)
print("Targets:", y.shape)
X = np.delete(data, 0, 1)
X = np.array(X, dtype=dtype)
print("Samples:", X.shape)

file_npy = os.path.splitext(args.file)[0] + ".npy"
print("Dataset file name (npy):", file_npy)

with open(file_npy, "wb") as f:
    np.save(f, y)
    np.save(f, X)

print("Dataset converted")
