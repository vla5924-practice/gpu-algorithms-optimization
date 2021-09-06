from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark.sql import Row
from pyspark.sql import SparkSession

from ..common import argparser, dataset, utils
from ..common.timer import Timer


spark = SparkSession.builder.appName("ml-benchmark-als").config("spark.executor.resource.gpu.amount", 1).getOrCreate()
args = argparser.build_parser(test_file=False, test=False).parse_args()

print("Fit dataset:", args.fit_file)

lines = spark.read.text(args.fit_file).rdd
parts = lines.map(lambda row: row.value.split("::"))
ratingsRDD = parts.map(lambda p: Row(userId=int(p[0]), movieId=int(p[1]),
                                     rating=float(p[2]), timestamp=int(p[3])))
ratings = spark.createDataFrame(ratingsRDD)

if 0 < args.fit_size < 1:
    (training, test) = ratings.randomSplit([args.fit_size, 1 - args.fit_size])
else:
    training = ratings
    test = ratings
utils.print_metric("Fit size", "FSZ", args.fit_size)

# Build the recommendation model using ALS on the training data
# Note we set cold start strategy to 'drop' to ensure we don't get NaN evaluation metrics
timer = Timer()
als = ALS(maxIter=5, regParam=0.01, userCol="userId", itemCol="movieId", ratingCol="rating",
          coldStartStrategy="drop")
model = als.fit(training)
utils.print_metric("Fit time", "FIT", timer.count())

# Evaluate the model by computing the RMSE on the test data
predictions = model.transform(test)
evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating",
                                predictionCol="prediction")
rmse = evaluator.evaluate(predictions)
utils.print_metric("Mean-squared error", "MSE", rmse)

# Generate top 10 movie recommendations for each user
# userRecs = model.recommendForAllUsers(10)
# Generate top 10 user recommendations for each movie
# movieRecs = model.recommendForAllItems(10)
