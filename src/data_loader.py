from pyspark.sql import SparkSession

# Create Spark Session
spark = SparkSession.builder \
    .appName("ECommerceSalesAnalysis") \
    .master("local[*]") \
    .getOrCreate()

# Load CSV dataset
df = spark.read.csv(
    "dataset/online_retail.csv",
    header=True,
    inferSchema=True
)

# Display first 10 records
print("\n========== FIRST 10 RECORDS ==========")
df.show(10)

# Display dataset structure
print("\n========== DATASET SCHEMA ==========")
df.printSchema()

# Count total records
print("\n========== DATASET INFORMATION ==========")
print("Total Records:", df.count())

print("Total Columns:", len(df.columns))

# Stop Spark
spark.stop()

