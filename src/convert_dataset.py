import pandas as pd

# Read Excel dataset
df = pd.read_excel("dataset/Online Retail.xlsx")

# Convert Excel to CSV
df.to_csv("dataset/online_retail.csv", index=False)

print("Dataset converted successfully!")

print("Total Rows:", len(df))
print("Total Columns:", len(df.columns))

print("\nColumn Names:")
print(df.columns.tolist())
