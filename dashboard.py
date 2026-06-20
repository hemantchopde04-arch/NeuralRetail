import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="NeuralRetail Dashboard", layout="wide")

st.title("🛒 NeuralRetail Dashboard")

# Load Data
csv_file = os.path.join(os.path.dirname(__file__), "online_retail_cleaned.csv")
df = pd.read_csv(csv_file)

# KPI Cards
total_revenue = df["total_price"].sum()
total_customers = df["customer_id"].nunique()
total_orders = df["invoice"].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"${total_revenue:,.0f}")
col2.metric("Total Customers", total_customers)
col3.metric("Total Orders", total_orders)

# RFM Analysis
rfm = df.groupby("customer_id").agg({
    "invoice": "count",
    "total_price": "sum"
})

rfm.columns = ["Frequency", "Monetary"]

st.header("Customer RFM Analysis")
st.dataframe(rfm.head(10))

# Customer Search
st.header("Customer Search")

customer_id = st.number_input(
    "Enter Customer ID",
    min_value=int(df["customer_id"].min()),
    max_value=int(df["customer_id"].max()),
    value=int(df["customer_id"].min())
)

if customer_id in rfm.index:
    st.write("Customer Details")
    st.dataframe(rfm.loc[[customer_id]])

# Customer Segmentation
st.header("Customer Segments")

rfm["Segment"] = "Regular Customer"

rfm.loc[
    (rfm["Frequency"] >= rfm["Frequency"].quantile(0.75)) &
    (rfm["Monetary"] >= rfm["Monetary"].quantile(0.75)),
    "Segment"
] = "VIP Customer"

rfm.loc[
    (rfm["Frequency"] <= rfm["Frequency"].quantile(0.25)) &
    (rfm["Monetary"] <= rfm["Monetary"].quantile(0.25)),
    "Segment"
] = "Low Value Customer"

segment_count = rfm["Segment"].value_counts()

st.bar_chart(segment_count)

st.dataframe(
    rfm[["Frequency", "Monetary", "Segment"]].head(20)
)

# Revenue by Country
st.header("Top Revenue Countries")

revenue_country = (
    df.groupby("country")["total_price"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(revenue_country)

# Product Revenue
st.header("Top Products By Revenue")

product_revenue = (
    df.groupby("description")["total_price"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(product_revenue)

# Customer Revenue
st.header("Top Customers By Revenue")

customer_revenue = (
    df.groupby("customer_id")["total_price"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(customer_revenue)

# Inventory Analysis
st.header("Inventory Analysis")

inventory = (
    df.groupby("description")["quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(inventory)

inventory_table = inventory.reset_index()
inventory_table.columns = ["Product", "Units Sold"]

st.dataframe(inventory_table)

st.success("Dashboard Loaded Successfully!")