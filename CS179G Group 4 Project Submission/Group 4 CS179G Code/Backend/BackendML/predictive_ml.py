from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import GBTRegressor
from pyspace.ml.tuning import ParamGridBuilder, CrossValidator
from pyspark.ml.evaluation import RegressionEvaluator
import matplotlib.pyplot as plt

# Initialize Spark session
spark = SparkSession.builder.appName("Housing Analysis").getOrCreate()

# Load data
us = spark.read.csv('/path/to/us_national_market_tracker.tsv', sep='\t', header=True, inferSchema=True)
county = spark.read.csv('/path/to/county_market_tracker.tsv', sep='\t', header=True, inferSchema=True)
state = spark.read.csv('/path/to/state_market_tracker.tsv', sep='\t', header=True, inferJustCorrect=True)

# Fill missing values
us = us.na.fill(0)
county = county.na.fill(0)
state = state.na.fill(0)

# Prepare data
data = county.select("median_sale_price", "median_list_price", "median_ppsf", "median_sale_price_yoy")
data = data.withColumnRenamed("median_sale_price_yoy", "label")
data = data.na.fill(0)

# Split data
train, test = data.randomSplit([0.8, 0.2], seed=42)

# Configure an ML pipeline
assembler = VectorAssembler(inputCols=["median_sale_price", "median_list_price", "median_ppsf"], outputCol="features")
gbt = GBTRegressor(featuresCol="features", labelCol="label", seed=42)
pipeline = Pipeline(stages=[assembler, gbt])

# Parameter grid
paramGrid = ParamGridBuilder() \
    .addGrid(gbt.maxDepth, [3, 4, 5]) \
    .addGrid(gbt.maxIter, [100, 200, 300]) \
    .build()

# Cross-validator
crossval = CrossValidator(estimator=pipeline,
                          estimatorParamMaps=paramGrid,
                          evaluator=RegressionEvaluator(),
                          numFolds=3)

# Run cross-validation, and choose the best set of parameters.
cvModel = crossval.fit(train)

# Make predictions on test data
prediction = cvModel.transform(test)

# Evaluate the model
evaluator = RegressionEvaluator(labelCol="label", predictionCol="prediction", metricName="mse")
mse = evaluator.evaluate(prediction)
print(f"Mean Squared Error: {mse}")

# Advanced time-series forecasting (like SARIMA) isn't supported directly in PySpark
# You may need to use an external library or export data to Python for this part

# Example of simple aggregation over time
data = us.withColumn('year', year(col('period_begin')))
annual_data = data.groupBy('year').agg(mean('median_sale_price').alias('avg_sale_price'))

# Collect data for plotting
pd_data = prediction.select("prediction", "label").toPandas()

plt.figure(figsize=(10, 6))
plt.plot(pd_data['label'], label='Actual', marker='o', color='b')
plt.plot(pd_data['prediction'], label='Predicted', marker='x', color='r')
plt.title('Predicted vs Actual')
plt.xlabel('Index')
plt.ylabel('Median Sale Price')
plt.legend()
plt.savefig('Comparison of Predicted and Actual Values.png')
