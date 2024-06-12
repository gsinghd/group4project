from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, when, month
from pyspark.ml.feature import StringIndexer, VectorAssembler
from pyspark.ml.classification import RandomForestClassifier
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.regression import LinearRegression

# Initialize Spark session
spark = SparkSession.builder.appName("Socioeconomic and Real Estate Market Analysis").getOrCreate()

# Load data
county = spark.read.csv('/home/cs179g/workspace/ml_analysis/filtered_data.csv/state=California/part-00000-9530e46c-6595-48ee-84e8-637ce473b6b8.c000.csv', header=True, sep='\t', inferSchema=True)
county = county.na.fill(0)

# Extract year from 'period_begin'
county = county.withColumn("year", year("period_begin"))

# Create socioeconomic classes based on the median sale price
county = county.withColumn("soc_eco_class", when(col("median_sale_price") < 200000, "Low")
                                              .when(col("median_sale_price") < 400000, "Medium")
                                              .otherwise("High"))

# Encode categorical data
indexer = StringIndexer(inputCols=["region", "state_code", "property_type"], outputCols=["region_indexed", "state_code_indexed", "property_type_indexed"])
county = indexer.fit(county).transform(county)

# Assemble features
feature_cols = ["price_drops", "median_sale_price", "median_dom", "region_indexed", "state_code_indexed", "property_type_indexed"]
assembler = VectorAssembler(inputCols=feature_cols, outputCol="features")
county = assembler.transform(county)

# Split the data into training and test sets
train, test = county.randomSplit([0.7, 0.3], seed=42)

# Initialize and train the classifier
classifier = RandomForestClassifier(labelCol="soc_eco_class", featuresCol="features", numTrees=100, seed=42)
model = classifier.fit(train)

# Predictions on test set
predictions = model.transform(test)

# Evaluate the model
evaluator = MulticlassClassificationEvaluator(labelCol="soc_eco_class", predictionCol="prediction", metricName="accuracy")
accuracy = evaluator.evaluate(predictions)
print("Classification Accuracy: ", accuracy)

# Assuming 'predicted_class' needs to be used for further analysis
from pyspark.ml.feature import IndexToString
converter = IndexToString(inputCol="prediction", outputCol="predicted_class", labels=model.labels)
predictions = converter.transform(predictions)

# Calculate trends over time
trends_over_time = predictions.groupBy("year", "predicted_class").count()

# Linear Regression Forecasting for future years
lr = LinearRegression(featuresCol="features", labelCol="count")
lrModel = lr.fit(train)  # Train on the actual data

# Forecast future values
forecast = lrModel.transform(test)

# Convert forecast to Pandas for visualization (if necessary)
pd_forecast = forecast.select("year", "predicted_class", "prediction").toPandas()

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.plot(pd_forecast['year'], pd_forecast['predicted_class'], label='Forecast')
plt.title('Forecasted Socioeconomic Trends')
plt.xlabel('Year')
plt.ylabel('Number of Regions')
plt.legend()
plt.savefig('Forecasted Socioeconomic Trends.png')

# Shut down Spark session
spark.stop()
