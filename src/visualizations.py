
from pyspark.sql import SparkSession
from pyspark.sql.functions import sum, desc, date_format
import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
import os

# Create Spark Session
spark = SparkSession.builder \
    .appName("ECommerceSalesVisualization") \
    .master("local[*]") \
    .config("spark.hadoop.fs.defaultFS", "file:///") \
    .getOrCreate()
# Load cleaned dataset
df = spark.read.parquet("outputs/cleaned_data")

# Create charts folder
os.makedirs("outputs/charts", exist_ok=True)

print("\nGenerating E-Commerce Sales Charts...")

# 1. Top 10 Selling Products
top_products = df.groupBy("Description") \
    .agg(sum("Quantity").alias("Total_Quantity")) \
    .orderBy(desc("Total_Quantity")) \
    .limit(10).toPandas()

plt.figure(figsize=(12, 6))
plt.barh(
    top_products["Description"],
    top_products["Total_Quantity"]
)
plt.xlabel("Quantity Sold")
plt.ylabel("Product")
plt.title("Top 10 Selling Products")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("outputs/charts/top_products.png")
plt.close()

print("Top products chart created!")

# 2. Monthly Sales Trend
monthly_sales = df.withColumn(
    "Month",
    date_format("InvoiceDate", "yyyy-MM")
).groupBy("Month") \
 .agg(sum("Revenue").alias("Revenue")) \
 .orderBy("Month").toPandas()

plt.figure(figsize=(12, 6))
plt.plot(
    monthly_sales["Month"],
    monthly_sales["Revenue"],
    marker="o"
)
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.title("Monthly Sales Trend")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/charts/monthly_sales.png")
plt.close()

print("Monthly sales chart created!")

# 3. Country-wise Revenue
country_sales = df.groupBy("Country") \
    .agg(sum("Revenue").alias("Revenue")) \
    .orderBy(desc("Revenue")) \
    .limit(10).toPandas()

plt.figure(figsize=(12, 6))
plt.bar(
    country_sales["Country"],
    country_sales["Revenue"]
)
plt.xlabel("Country")
plt.ylabel("Revenue")
plt.title("Top 10 Countries by Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("outputs/charts/country_sales.png")
plt.close()

print("Country sales chart created!")

# 4. Top 10 Customers
customer_sales = df.filter(
    df.CustomerID.isNotNull()
).groupBy("CustomerID") \
 .agg(sum("Revenue").alias("Revenue")) \
 .orderBy(desc("Revenue")) \
 .limit(10).toPandas()

plt.figure(figsize=(12, 6))
plt.bar(
    customer_sales["CustomerID"].astype(str),
    customer_sales["Revenue"]
)
plt.xlabel("Customer ID")
plt.ylabel("Revenue")
plt.title("Top 10 Customers by Spending")
plt.tight_layout()
plt.savefig("outputs/charts/top_customers.png")
plt.close()

print("Customer sales chart created!")

print("\nAll charts generated successfully!")
print("Chart location: outputs/charts/")

spark.stop()
