
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, trim, upper, when
)

# Create Spark Session
spark = SparkSession.builder \
    .appName("ECommerceDataCleaning") \
    .master("local[*]") \
    .config("spark.hadoop.fs.defaultFS", "file:///") \
    .getOrCreate()
# Load dataset
df = spark.read.csv(
    "dataset/online_retail.csv",
    header=True,
    inferSchema=True
)

print("\n========== ORIGINAL DATA ==========")
print("Original Records:", df.count())

# 1. Remove duplicate records
df = df.dropDuplicates()

# 2. Clean text columns
df = df.withColumn("Description", trim(col("Description"))) \
       .withColumn("Country", trim(col("Country"))) \
       .withColumn("InvoiceNo", trim(col("InvoiceNo")))

# 3. Remove records with missing essential values
df = df.filter(
    col("InvoiceNo").isNotNull() &
    col("StockCode").isNotNull() &
    col("Description").isNotNull() &
    col("Quantity").isNotNull() &
    col("UnitPrice").isNotNull() &
    col("InvoiceDate").isNotNull() &
    col("Country").isNotNull()
)

# 4. Identify cancelled invoices
df = df.withColumn(
    "InvoiceNo",
    upper(col("InvoiceNo"))
)

cancelled_df = df.filter(
    col("InvoiceNo").startswith("C")
)

print("\nCancelled Invoice Records:", cancelled_df.count())

# 5. Keep normal sales transactions
sales_df = df.filter(
    (~col("InvoiceNo").startswith("C")) &
    (col("Quantity") > 0) &
    (col("UnitPrice") > 0)
)

# 6. Calculate revenue
sales_df = sales_df.withColumn(
    "Revenue",
    col("Quantity") * col("UnitPrice")
)

print("\n========== CLEANED DATA ==========")
print("Cleaned Sales Records:", sales_df.count())

# 7. Display cleaned records
sales_df.show(10)

# 8. Save cleaned data in Parquet format
sales_df.write \
    .mode("overwrite") \
    .parquet("outputs/cleaned_data")

print("\nCleaned dataset saved successfully!")

spark.stop()
