from pyspark.ml.clustering import KMeans
from pyspark.ml.evaluation import ClusteringEvaluator
from pyspark.sql import SparkSession

from common import argparser
from common.timer import Timer


spark = SparkSession.builder.appName("ml-benchmark-kmeans").getOrCreate()
args = argparser.build_parser(test_file=False, test=False).parse_args()

print("Fit dataset:", args.fit_file)

X = spark.read.format("libsvm").load(args.fit_file)

timer = Timer()
kmeans = KMeans().setK(2).setSeed(777)
model = kmeans.fit(X)
print("Fit time:", timer.count())

# Make predictions
predictions = model.transform(X)

# Evaluate clustering by computing Silhouette score
evaluator = ClusteringEvaluator()
silhouette = evaluator.evaluate(predictions)
print("Silhouette with squared euclidean distance = " + str(silhouette))

# Show the result
centers = model.clusterCenters()
print("Cluster Centers:")
for center in centers:
    print(center)
