#preprocessing dataset for machine learning
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.functions import avg
from pyspark.sql import functions as F

spark = SparkSession.builder.appName("preprocess_data").getOrCreate()
file_path = "/home/cs179g/workspace/output_cleaned/zip_code_market.csv"
df = spark.read.csv(file_path, header=True, inferSchema=True)
df.printSchema()

columns_needed = ['period_begin', 'period_end', 'region_type', 'region', 'state', 'state_code', 'property_type', 'parent_metro_region', 'last_updated', 'price_drops', 'median_sale_price', 'median_dom']
filtered_df = df.select(columns_needed)
filtered_df.printSchema()
filtered_df.show(1)

#save dataframe as csv
filtered_df.write.csv("/home/cs179g/workspace/ml_analysis/filtered_data.csv", header = True, mode = "overwrite")