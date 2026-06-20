from fastapi import FastAPI
import pandas as pd
import os

app = FastAPI(title="NeuralRetail API")

# CSV Path
csv_file = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "online_retail_cleaned.csv"
)

df = pd.read_csv(csv_file)

@app.get("/")
def home():
    return {
        "message": "NeuralRetail API Running"
    }

@app.get("/customers")
def customers():
    return {
        "total_customers": int(df["customer_id"].nunique())
    }

@app.get("/revenue")
def revenue():
    return {
        "total_revenue": float(df["total_price"].sum())
    }

@app.get("/orders")
def orders():
    return {
        "total_orders": int(df["invoice"].nunique())
    }

@app.get("/top-country")
def top_country():
    country = (
        df.groupby("country")["total_price"]
        .sum()
        .sort_values(ascending=False)
        .head(1)
    )

    return {
        "country": str(country.index[0]),
        "revenue": float(country.iloc[0])
    }

@app.get("/top-product")
def top_product():
    product = (
        df.groupby("description")["total_price"]
        .sum()
        .sort_values(ascending=False)
        .head(1)
    )

    return {
        "product": str(product.index[0]),
        "revenue": float(product.iloc[0])
    }

@app.get("/health")
def health():
    return {
        "status": "API Running Successfully"
    }