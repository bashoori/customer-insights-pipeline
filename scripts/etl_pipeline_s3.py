"""
customer_insights_pipeline/scripts/etl_pipeline.py

ETL script that reads customer, store sales, and online order data from AWS S3,
performs transformations, and outputs a unified fact table for reporting.
"""

import pandas as pd
import json
import boto3
from io import StringIO, BytesIO

# Set S3 bucket and prefix
bucket_name = "bashoori-s3"
prefix = "customer-purchase-data/"

# Initialize S3 client
s3 = boto3.client("s3")

# Helper function to read CSV from S3
def read_csv_from_s3(key):
    response = s3.get_object(Bucket=bucket_name, Key=prefix + key)
    return pd.read_csv(response["Body"])

# Helper function to read JSON from S3
def read_json_from_s3(key):
    response = s3.get_object(Bucket=bucket_name, Key=prefix + key)
    return json.load(response["Body"])

# Step 1: Load data from S3
df_customers = read_csv_from_s3("mock_customers.csv")
df_store = read_csv_from_s3("mock_store_sales.csv")
raw_json = read_json_from_s3("mock_online_orders.json")

# Flatten online orders
flattened_orders = []
for order in raw_json:
    for item in order["items"]:
        flattened_orders.append({
            "order_id": order["order_id"],
            "customer_id": order["customer_id"],
            "product_id": item["product_id"],
            "quantity": item["quantity"],
            "price": item["price"],
            "timestamp": order["order_date"],
            "total_value": round(item["price"] * item["quantity"], 2)
        })
df_online = pd.DataFrame(flattened_orders)

# Step 2: Process store sales
df_store["total_value"] = round(df_store["quantity"] * df_store["price"], 2)

# Step 3: Combine online and store sales
df_combined = pd.concat([df_store, df_online], ignore_index=True)

# Step 4: Join with customer data
df_fact_orders = df_combined.merge(df_customers, on="customer_id", how="left")

# Step 5: Save locally to outputs
output_path = "../outputs/fact_orders_from_s3.csv"
df_fact_orders.to_csv(output_path, index=False)

print("✅ ETL complete. Output saved to:", output_path)
