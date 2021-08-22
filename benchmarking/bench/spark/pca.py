from pyspark.sql import SparkSession
from pyspark.mllib.util import MLUtils
from pyspark import SparkContext

from .. import common


spark = SparkSession.builder.appName("ml-benchmark-pca").getOrCreate()
sc = spark.sparkContext

args = common.build_argument_parser(test_file=False, test=False).parse_args()

print("Fit dataset:", args.fit_file)

X = MLUtils.loadLibSVMFile(sc, args.fit_file)

timer = common.Timer()
X.toDF().computePrincipalComponents(2)
print("Fit time:", timer.count())
