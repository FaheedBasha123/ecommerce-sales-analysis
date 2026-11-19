
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Page configuration
st.set_page_config(
    page_title="E-Commerce Sales Analytics",
    page_icon="🛒",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
[data-testid="stMetric"] {
    background-color: #1c2333;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #303b50;
}
</style>
""", unsafe_allow_html=True)

# Title
st.title("🛒 E-Commerce Sales Analytics")
st.caption("Big Data Analysis using Apache PySpark")

# Load cleaned dataset
@st.cache_data
def load_data():
    return pd.read_parquet("outputs/cleaned_data")

if not os.path.exists("outputs/cleaned_data"):
    st.error("Cleaned dataset not found. Run the data cleaning module first.")
    st.stop()

df = load_data()

# Convert date column
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], errors="coerce")

# Sidebar filters
st.sidebar.header("Dashboard Filters")

countries = ["All"] + sorted(df["Country"].dropna().unique().tolist())
selected_country = st.sidebar.selectbox("Select Country", countries)

filtered_df = df.copy()

if selected_country != "All":
    filtered_df = filtered_df[
        filtered_df["Country"] == selected_country
    ]

# KPI calculations
total_revenue = filtered_df["Revenue"].sum()
total_orders = filtered_df["InvoiceNo"].nunique()
total_customers = filtered_df["CustomerID"].nunique()
average_order_value = (
    filtered_df.groupby("InvoiceNo")["Revenue"].sum().mean()
)

# KPI cards
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"£{total_revenue:,.2f}")
col2.metric("Total Orders", f"{total_orders:,}")
col3.metric("Total Customers", f"{total_customers:,}")
col4.metric("Average Order Value", f"£{average_order_value:,.2f}")

st.divider()

# Monthly sales trend
st.subheader("📈 Monthly Sales Trend")

monthly_sales = (
    filtered_df
    .dropna(subset=["InvoiceDate"])
    .assign(Month=lambda x: x["InvoiceDate"].dt.to_period("M").astype(str))
    .groupby("Month", as_index=False)["Revenue"]
    .sum()
)

fig_monthly = px.line(
    monthly_sales,
    x="Month",
    y="Revenue",
    markers=True,
    title="Monthly Revenue"
)

st.plotly_chart(fig_monthly, use_container_width=True)

# Product and country analysis
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top 10 Products")

    top_products = (
        filtered_df.groupby("Description", as_index=False)["Revenue"]
        .sum()
        .nlargest(10, "Revenue")
    )

    fig_products = px.bar(
        top_products,
        x="Revenue",
        y="Description",
        orientation="h",
        title="Products by Revenue"
    )

    st.plotly_chart(fig_products, use_container_width=True)

with col2:
    st.subheader("🌍 Top 10 Countries")

    country_sales = (
        filtered_df.groupby("Country", as_index=False)["Revenue"]
        .sum()
        .nlargest(10, "Revenue")
    )

    fig_country = px.bar(
        country_sales,
        x="Country",
        y="Revenue",
        title="Revenue by Country"
    )

    st.plotly_chart(fig_country, use_container_width=True)

# Top customers
st.subheader("👥 Top 10 Customers")

top_customers = (
    filtered_df.dropna(subset=["CustomerID"])
    .groupby("CustomerID", as_index=False)["Revenue"]
    .sum()
    .nlargest(10, "Revenue")
)

fig_customers = px.bar(
    top_customers,
    x="CustomerID",
    y="Revenue",
    title="Highest Spending Customers"
)

st.plotly_chart(fig_customers, use_container_width=True)

# Dataset preview
with st.expander("View Dataset"):
    st.dataframe(filtered_df.head(100), use_container_width=True)

st.success("Dashboard loaded successfully!")
