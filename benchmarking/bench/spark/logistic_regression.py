from pyspark.ml.classification import LogisticRegression
from pyspark.sql import SparkSession

from common import argparser, utils
from common.timer import Timer


spark = SparkSession.builder.appName(
    "ml-benchmark-logistic-regression").getOrCreate()
args = argparser.build_parser(test_file=False, test=False).parse_args()

print("Fit dataset:", args.fit_file)

X = spark.read.format("libsvm").load(args.fit_file)

timer = Timer()
kmeans = LogisticRegression()
model = kmeans.fit(X)
print("Fit time:", timer.count())

utils.print_params({
    "Coefficients": model.coefficients,
    "Intercept": model.intercept,
})
