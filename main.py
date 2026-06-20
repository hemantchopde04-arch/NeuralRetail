import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("../online_retail_cleaned.csv")

# RFM Analysis
rfm = df.groupby("customer_id").agg({
    "invoice": "count",
    "total_price": "sum"
})

rfm.columns = ["Frequency", "Monetary"]

rfm["F_Score"] = pd.qcut(
    rfm["Frequency"],
    4,
    labels=[1, 2, 3, 4]
)

rfm["M_Score"] = pd.qcut(
    rfm["Monetary"],
    4,
    labels=[1, 2, 3, 4]
)

rfm["RFM_Score"] = (
    rfm["F_Score"].astype(str) +
    rfm["M_Score"].astype(str)
)

def segment(score):
    if score == "44":
        return "VIP Customer"
    elif score in ["43", "34", "33"]:
        return "Loyal Customer"
    elif score in ["32", "23", "24"]:
        return "Regular Customer"
    else:
        return "Low Value Customer"

rfm["Segment"] = rfm["RFM_Score"].apply(segment)

print("RFM Table:")
print(rfm.head(10))

print("\nCustomer Segments:")
print(rfm[["Frequency", "Monetary", "RFM_Score", "Segment"]].head(10))

print("\nTop 10 Customers:")

top_customers = rfm.sort_values(
    by=["Monetary", "Frequency"],
    ascending=False
)

print(top_customers.head(10))

rfm.to_csv("RFM_Segmentation.csv")

print("\nRFM Segmentation file saved successfully!")

# Revenue by Country

print("\nTop 10 Revenue Countries:")

revenue_country = (
    df.groupby("country")["total_price"]
    .sum()
    .sort_values(ascending=False)
)

print(revenue_country.head(10))

top10_country = revenue_country.head(10)

plt.figure(figsize=(12,5))
top10_country.plot(kind="bar")

plt.title("Top 10 Revenue Countries")
plt.xlabel("Country")
plt.ylabel("Revenue")

for i, v in enumerate(top10_country):
    plt.text(i, v, str(int(v)), ha="center")

plt.tight_layout()
plt.show()

# Top Products by Revenue

print("\nTop 10 Products By Revenue:")

product_revenue = (
    df.groupby("description")["total_price"]
    .sum()
    .sort_values(ascending=False)
)

print(product_revenue.head(10))

top_products = product_revenue.head(10)

plt.figure(figsize=(12,5))
top_products.plot(kind="bar")

plt.title("Top 10 Products By Revenue")
plt.xlabel("Product")
plt.ylabel("Revenue")

plt.xticks(rotation=45)

for i, v in enumerate(top_products):
    plt.text(i, v, str(int(v)), ha="center")

plt.tight_layout()
plt.show()

# Top Customers by Revenue

print("\nTop 10 Customers By Revenue:")

customer_revenue = (
    df.groupby("customer_id")["total_price"]
    .sum()
    .sort_values(ascending=False)
)

print(customer_revenue.head(10))

top_customers_revenue = customer_revenue.head(10)

plt.figure(figsize=(12,5))
top_customers_revenue.plot(kind="bar")

plt.title("Top 10 Customers By Revenue")
plt.xlabel("Customer ID")
plt.ylabel("Revenue")

for i, v in enumerate(top_customers_revenue):
    plt.text(i, v, str(int(v)), ha="center")

plt.tight_layout()
plt.show()

customer_revenue.head(10).to_csv(
    "Top_10_Customers_Revenue.csv"
)

print("\nWeek 2 Checkpoint Completed Successfully!")