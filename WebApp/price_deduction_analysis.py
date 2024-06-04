from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.functions import avg
from pyspark.sql import functions as F
from pyspark.sql.functions import col, year, month

spark = SparkSession.builder.appName("price_deduction_analysis").getOrCreate()
file_path = "/home/cs179g/workspace/output_cleaned/zip_code_market.csv"
df = spark.read.csv(file_path, header=True, inferSchema=True)
df.printSchema()

#price deduction analysis code
#(ran in pyspark shell)
#median_dom = median days on market
price_deduct_columns = ["median_sale_price", "median_list_price", "price_drops", "median_ppsf", "period_begin", "period_end", "region", "state", "property_type", "homes_sold", "median_dom", "last_updated"]
price_deduction_df = df.select(price_deduct_columns)
price_deduction_df.cache()
price_deduction_df.show()

#price change by state
price_deduction_df = price_deduction_df.withColumn("price_change", col("median_list_price") - col("median_sale_price"))
avg_price_change_by_state = price_deduction_df.groupBy("state").agg(avg("price_change").alias("avg_price_change"))
avg_price_change_by_state.show()
avg_price_change_by_state.write.csv("/home/cs179g/workspace/data/avg_price_change_by_state.csv", header=True, mode="overwrite")


#price change by region
avg_price_change_by_region = price_deduction_df.groupBy("region").agg(avg("price_change").alias("avg_price_change"))
avg_price_change_by_region.show()
avg_price_change_by_region.write.csv("/home/cs179g/workspace/data/avg_price_change_by_region.csv", header=True, mode="overwrite")


spark.stop()