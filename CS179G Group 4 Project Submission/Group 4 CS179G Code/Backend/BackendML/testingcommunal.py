from pyspark.sql import SparkSession, Window
from pyspark.sql.functions import col, year, lag, percent_rank, when
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml import Pipeline
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
import matplotlib.pyplot as plt

spark = SparkSession.builder.appName("Housing Market Prediction").getOrCreate()



county = spark.read.csv("/home/cs179g/workspace/ml_analysis/filtered_data.csv", header=True, inferSchema=True)
county = county.na.fill(0)
data = county.withColumn("year", year("period_begin"))

rank_spec = Window.partitionBy("state_code").orderBy("median_sale_price")
county = county.withColumn("percent_rank", percent_rank().over(rank_spec))
county = county.withColumn("soc_eco_class", when(col("percent_rank") < 0.33, "Low").when(col("percent_rank") < 0.67, "Medium").otherwise("High"))

# Encode categorical data
labelIndexer = StringIndexer(inputCol="soc_eco_class", outputCol="label").fit(county)
regionIndexer = StringIndexer(inputCol="region", outputCol="region_indexed")
vectorAssembler = VectorAssembler(
    inputCols=["median_sale_price", "homes_sold", "inventory", "months_of_supply", "region_indexed", "percent_rank"],
    outputCol="features"
)

# Define the model
rf = RandomForestClassifier(featuresCol='features', labelCol='label', numTrees=100, maxBins=20000, seed=42)

# Create a pipeline
pipeline = Pipeline(stages=[regionIndexer, labelIndexer, vectorAssembler, rf])

# Split the data into training and testing sets
(train_data, test_data) = county.randomSplit([0.7, 0.3], seed=42)

# Fit the model
model = pipeline.fit(train_data)

# Predictions
predictions = model.transform(test_data)

# Evaluate the model
evaluator = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="accuracy")
accuracy = evaluator.evaluate(predictions)
print("Accuracy:", accuracy)

# Feature Importances
rf_model = model.stages[-1]
importances = rf_model.featureImportances
feature_importances = dict(zip(["median_sale_price", "median_list_price", "region_indexed", "homes_sold"], importances))
print("Feature Importances:", feature_importances)





'''
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, to_date

# Initialize Spark session
spark = SparkSession.builder.appName("Socioeconomic and Real Estate Market Analysis").getOrCreate()

# Load data
county = spark.read.csv('/home/cs179g/workspace/ml_analysis/filtered_data.csv/state=California/part-00000-9530e46c-6595-48ee-84e8-637ce473b6b8.c000.csv', header=True, sep='\t', inferSchema=True)

# Print the schema to check column names and types
county.printSchema()

# Convert 'period_begin' to a date type if necessary
# Ensure the column 'period_begin' is correctly referenced using col function
county = county.withColumn("period_begin", to_date(col("period_begin"), "yyyy-MM-dd"))

# Now extract the year from the 'period_begin' date
county = county.withColumn("year", year(col("period_begin")))

# Show some data to ensure transformations are correct
county.show(5)

# Shut down Spark session
spark.stop()

'''

