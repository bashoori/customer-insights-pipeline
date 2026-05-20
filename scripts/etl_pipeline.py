"""
customer_insights_pipeline/scripts/etl_pipeline.py

This script performs the ETL process for unifying customer transactions from online (JSON), in-store (CSV),
and CRM (CSV) data into a single FactOrders table. The output is stored as a CSV file ready for analytics
and dashboarding. Built for execution in GitHub Codespaces or any local Python environment.
"""

import pandas as pd
import json

# Step 1: Load source files
customer_path = "../data/mock_customers.csv"
store_sales_path = "../data/mock_store_sales.csv"
online_orders_path = "../data/mock_online_orders.json"
output_path = "../outputs/fact_orders.csv"

# Load customer data (CRM) as DataFrame
df_customers = pd.read_csv(customer_path)

# Load store sales CSV (from POS system)
df_store = pd.read_csv(store_sales_path)

# Load and flatten online orders JSON
with open(online_orders_path, "r") as f:
    raw_json = json.load(f)

flattened_orders = []
for order in raw_json:
    for item in order["items"]:
        # Extract and flatten nested JSON structure
        flattened_orders.append({
            "order_id": order["order_id"],
            "customer_id": order["customer_id"],
            "product_id": item["product_id"],
            "quantity": item["quantity"],
            "price": item["price"],
            "timestamp": order["order_date"],
            "total_value": round(item["price"] * item["quantity"], 2)
        })

# Convert to DataFrame
df_online = pd.DataFrame(flattened_orders)

# Step 2: Clean and standardize in-store data
df_store["total_value"] = round(df_store["quantity"] * df_store["price"], 2)

# Step 3: Combine store and online data
df_combined = pd.concat([df_store, df_online], ignore_index=True)

# Step 4: Join with customer master data
df_fact_orders = df_combined.merge(df_customers, on="customer_id", how="left")

# Step 5: Output result to CSV
df_fact_orders.to_csv(output_path, index=False)

print("✅ ETL complete. Output saved to:", output_path)
