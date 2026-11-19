
from pyspark.sql import SparkSession

# Create Spark Session
spark = SparkSession.builder \
    .appName("ECommerceSparkSQL") \
    .master("local[*]") \
    .config("spark.hadoop.fs.defaultFS", "file:///") \
    .getOrCreate()
# Load cleaned dataset
df = spark.read.parquet("outputs/cleaned_data")

# Create SQL temporary view
df.createOrReplaceTempView("sales")

print("\n========== E-COMMERCE SPARK SQL ANALYSIS ==========")

# 1. Total Revenue
print("\n1. TOTAL REVENUE")

spark.sql("""
    SELECT ROUND(SUM(Revenue), 2) AS Total_Revenue
    FROM sales
""").show()

# 2. Total Orders
print("\n2. TOTAL ORDERS")

spark.sql("""
    SELECT COUNT(DISTINCT InvoiceNo) AS Total_Orders
    FROM sales
""").show()

# 3. Top 10 Products
print("\n3. TOP 10 PRODUCTS")

spark.sql("""
    SELECT
        Description,
        SUM(Quantity) AS Total_Quantity,
        ROUND(SUM(Revenue), 2) AS Total_Revenue
    FROM sales
    GROUP BY Description
    ORDER BY Total_Quantity DESC
    LIMIT 10
""").show(truncate=False)

# 4. Country-wise Revenue
print("\n4. COUNTRY-WISE REVENUE")

spark.sql("""
    SELECT
        Country,
        ROUND(SUM(Revenue), 2) AS Revenue
    FROM sales
    GROUP BY Country
    ORDER BY Revenue DESC
    LIMIT 10
""").show(truncate=False)

# 5. Monthly Revenue
print("\n5. MONTHLY REVENUE")

spark.sql("""
    SELECT
        DATE_FORMAT(InvoiceDate, 'yyyy-MM') AS Month,
        ROUND(SUM(Revenue), 2) AS Monthly_Revenue
    FROM sales
    GROUP BY DATE_FORMAT(InvoiceDate, 'yyyy-MM')
    ORDER BY Month
""").show(50)

# 6. Top 10 Customers
print("\n6. TOP 10 CUSTOMERS")

spark.sql("""
    SELECT
        CustomerID,
        ROUND(SUM(Revenue), 2) AS Total_Spending
    FROM sales
    WHERE CustomerID IS NOT NULL
    GROUP BY CustomerID
    ORDER BY Total_Spending DESC
    LIMIT 10
""").show()

# 7. Average Order Value
print("\n7. AVERAGE ORDER VALUE")

spark.sql("""
    SELECT ROUND(AVG(Order_Revenue), 2) AS Average_Order_Value
    FROM (
        SELECT
            InvoiceNo,
            SUM(Revenue) AS Order_Revenue
        FROM sales
        GROUP BY InvoiceNo
    )
""").show()

print("\nSPARK SQL ANALYSIS COMPLETED!")

spark.stop()
