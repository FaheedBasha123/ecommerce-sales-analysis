
from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, sum, countDistinct, avg,
    desc, date_format, round
)

# Create Spark Session
spark = SparkSession.builder \
    .appName("ECommerceSalesAnalysis") \
    .master("local[*]") \
    .config("spark.hadoop.fs.defaultFS", "file:///") \
    .getOrCreate()
# Load cleaned dataset
df = spark.read.parquet("outputs/cleaned_data")

print("\n========== E-COMMERCE SALES ANALYSIS ==========")

# 1. Total Revenue
total_revenue = df.agg(
    round(sum("Revenue"), 2).alias("Total_Revenue")
)

print("\n1. TOTAL REVENUE")
total_revenue.show()

# 2. Total Orders
total_orders = df.select(
    countDistinct("InvoiceNo").alias("Total_Orders")
)

print("\n2. TOTAL ORDERS")
total_orders.show()

# 3. Total Customers
total_customers = df.select(
    countDistinct("CustomerID").alias("Total_Customers")
)

print("\n3. TOTAL CUSTOMERS")
total_customers.show()

# 4. Total Products
total_products = df.select(
    countDistinct("StockCode").alias("Total_Products")
)

print("\n4. TOTAL PRODUCTS")
total_products.show()

# 5. Top 10 Selling Products
top_products = df.groupBy(
    "Description"
).agg(
    sum("Quantity").alias("Total_Quantity"),
    round(sum("Revenue"), 2).alias("Total_Revenue")
).orderBy(
    desc("Total_Quantity")
).limit(10)

print("\n5. TOP 10 SELLING PRODUCTS")
top_products.show(truncate=False)

# 6. Top 10 Customers
top_customers = df.filter(
    col("CustomerID").isNotNull()
).groupBy(
    "CustomerID"
).agg(
    round(sum("Revenue"), 2).alias("Total_Spending")
).orderBy(
    desc("Total_Spending")
).limit(10)

print("\n6. TOP 10 CUSTOMERS")
top_customers.show()

# 7. Country-wise Sales
country_sales = df.groupBy(
    "Country"
).agg(
    round(sum("Revenue"), 2).alias("Total_Revenue")
).orderBy(
    desc("Total_Revenue")
)

print("\n7. COUNTRY-WISE SALES")
country_sales.show(20, truncate=False)

# 8. Monthly Sales Analysis
monthly_sales = df.withColumn(
    "Month",
    date_format(col("InvoiceDate"), "yyyy-MM")
).groupBy(
    "Month"
).agg(
    round(sum("Revenue"), 2).alias("Monthly_Revenue")
).orderBy("Month")

print("\n8. MONTHLY SALES")
monthly_sales.show(50)

# 9. Average Order Value
order_revenue = df.groupBy(
    "InvoiceNo"
).agg(
    sum("Revenue").alias("Order_Revenue")
)

average_order_value = order_revenue.agg(
    round(avg("Order_Revenue"), 2).alias("Average_Order_Value")
)

print("\n9. AVERAGE ORDER VALUE")
average_order_value.show()

print("\nSALES ANALYSIS COMPLETED SUCCESSFULLY!")

spark.stop()
