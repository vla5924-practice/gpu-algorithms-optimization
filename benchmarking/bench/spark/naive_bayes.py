from pyspark.mllib.classification import NaiveBayes, NaiveBayesModel
from pyspark.mllib.util import MLUtils
from pyspark.sql import SparkSession
from pyspark import SparkContext

from common import argparser
from common.timer import Timer


spark = SparkSession.builder.appName("ml-benchmark-naive-bayes").getOrCreate()
sc = spark.sparkContext

args = argparser.build_parser().parse_args()

print("Fit dataset:", args.fit_file)

X = MLUtils.loadLibSVMFile(sc, args.fit_file)

timer = Timer()
model = NaiveBayes.train(X)
print("Fit time:", timer.count())

if args.test:
    print("Test dataset:", args.test_file)
    X_t = MLUtils.loadLibSVMFile(sc, args.test_file)

    timer = Timer()
    prediction_and_label = X_t.map(
        lambda p: (model.predict(p.features), p.label))
    print("Predicting time:", timer.count())

    accuracy = 1.0 * \
        prediction_and_label.filter(
            lambda pl: pl[0] == pl[1]).count() / X_t.count()
    print("Accuracy score: {}".format(accuracy))
