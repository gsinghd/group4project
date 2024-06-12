from pyspark.sql import SparkSession
from pyscraper.ml.feature import VectorAssembler
from pyspark.ml.regression import GBTRegressor
from pyspark.ml.evaluation import RegressionEvaluator
import matplotlib.pyplot as plt

# Initialize Spark session
spark = SparkSession.builder.appName("Median Sale Price Prediction").getOrCreate()

# Load data
us = spark.read.csv('/home/cs179g/workspace/data/us_national_market_tracker.tsv000', sep='\t', header=True, inferSchema=True)
county = spark.read.csv('/home/cs179g/workspace/data/county_market_tracker.tsv000', sep='\t', header=True, inferSchema=True)
state = spark.read.csv('/home/cs179g/workspace/data/state_market_tracker.tsv000', sep='\t', header=True, inferSchema=True)

# Fill missing values
us = us.na.fill(0)
county = county.na.fill(0)
state = state.na.fill(0)

# Select dataset
data = county
data.printSchema()  # To print the schema and verify column types

# Remove non-numeric columns
non_numeric_cols = [
    'period_begin', 'period_end', 'region_type', 'region', 'city', 'state', 'state_code', 
    'property_type', 'parent_metro_region', 'last_updated'
]
numeric_cols = [col for col in data.columns if col not in non_numeric_cols + ['median_sale_price']]
data = data.select(numeric_cols)

# Prepare features and labels
assembler = VectorAssembler(inputCols=numeric_cols, outputCol="features")
data = assembler.transform(data)
data = data.withColumn("label", data["median_sale_price"].cast("float"))

# Split data
(train, test) = data.randomSplit([0.8, 0.2], seed=42)

# Define model
gbt = GBTRegressor(featuresCol="features", labelCol="label", maxIter=10, seed=42)

# Train model
model = gbt.fit(train)

# Predictions
predictions = model.transform(test)

# Evaluate model
evaluator = RegressionEvaluator(labelCol="label", predictionCol="prediction", metricName="mse")
mse = evaluator.evaluate(predictions)
print(f"Mean Squared Error: {mse}")

# Plotting (requires conversion to Pandas)
pd_predictions = predictions.select("label", "prediction").toPandas()
plt.figure(figsize=(10, 6))
plt.plot(pd_predictions['label'][:100], label='Actual')
plt.plot(pd_predictions['prediction'][:100], label='Predicted')
plt.legend()
plt.title('Median Sale Price Prediction (as surrogate for Population)')
plt.xlabel('Sample')
plt.ylabel('Median Sale Price')
plt.show()
plt.savefig('Median Sale Price Prediction.png')