from pyspark.sql import SparkSession

# Create Spark Session
spark = SparkSession.builder \
    .appName("ECommerceSalesAnalysis") \
    .master("local[*]") \
    .getOrCreate()

print("================================")
print("E-Commerce Sales Analysis")
print("================================")

print("Spark Version:", spark.version)

print("Spark Session Created Successfully!")

# Stop Spark
spark.stop()
