from pyspark.ml.classification import LogisticRegression
from pyspark.sql import SparkSession

from .. import common


spark = SparkSession.builder.appName(
    "ml-benchmark-logistic-regression").getOrCreate()
args = common.build_argument_parser(test_file=False, test=False).parse_args()

print("Fit dataset:", args.fit_file)

X = spark.read.format("libsvm").load(args.fit_file)

timer = common.Timer()
kmeans = LogisticRegression()
model = kmeans.fit(X)
print("Fit time:", timer.count())

common.print_params({
    "Coefficients": model.coefficients,
    "Intercept": model.intercept,
})
