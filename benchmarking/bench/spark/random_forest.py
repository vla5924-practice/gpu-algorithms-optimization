from pyspark.ml.classification import RandomForestClassifier
from pyspark.sql import SparkSession

from ..common import argparser
from ..common.timer import Timer


spark = SparkSession.builder.appName(
    "ml-benchmark-random-forest").getOrCreate()
args = argparser.build_parser(test_file=False, test=False).parse_args()

print("Fit dataset:", args.fit_file)

X = spark.read.format("libsvm").load(args.fit_file)

timer = Timer()
rf = RandomForestClassifier()
model = rf.fit(X)
print("Fit time:", timer.count())
