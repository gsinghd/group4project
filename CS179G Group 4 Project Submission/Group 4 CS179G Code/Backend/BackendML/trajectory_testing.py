from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import LinearRegression
from pyspark.ml.evaluation import RegressionEvaluator

# Initialize Spark Session
spark = SparkSession.builder.appName("HousingMarketPrediction").getOrCreate()

# Load data
#data = spark.read.csv('/home/cs179g/workspace/ml_analysis/filtered_data.csv', header=True, sep='\t', inferSchema=True)
data_path = '/home/cs179g/workspace/ml_analysis/filtered_data.csv'  # Update this to your dataset's actual path
df = spark.read.csv(data_path, header=True, inferSchema=True)
clean_df = df.na.drop()


# Filter the dataset for county-level data if 'region_type' is available and includes 'county'
#df = df.filter(df['region_type'] == 'county')

# Feature Engineering: Select features and preprocess data
# Convert necessary features to numeric if not already and handle nulls or outliers if necessary
df = df.withColumn("median_sale_price", df["median_sale_price"].cast("float"))
df = df.withColumn("homes_sold", df["homes_sold"].cast("int"))

# Assuming 'region' represents the county
features = ["median_sale_price", "homes_sold", "new_listings", "inventory", "months_of_supply"]
assembler = VectorAssembler(inputCols=features, outputCol="features", handleInvalid="skip")

# Prepare the final dataframe for training
final_df = assembler.transform(df).select(col("features"), col("median_sale_price").alias("label"))

# Split the data into training and testing sets
train_data, test_data = final_df.randomSplit([0.7, 0.3])

# Model Training
lr = LinearRegression(featuresCol='features', labelCol='label')
lr_model = lr.fit(train_data)

# Evaluate the model
predictions = lr_model.transform(test_data)
evaluator = RegressionEvaluator(labelCol="label", predictionCol="prediction", metricName="rmse")
rmse = evaluator.evaluate(predictions)
print(f"Root Mean Squared Error (RMSE) on test data = {rmse}")

# Model usage for prediction
# Here, you could input new data in the same format to make future predictions
# example_new_data = ...
# prediction_result = lr_model.transform(example_new_data)

# Stop Spark session
spark.stop()
