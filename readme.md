# 📊 Customer Purchase Insights Pipeline

This project demonstrates an end-to-end ETL pipeline that integrates customer transactions from multiple sources: JSON-based online orders, CSV-based in-store transactions, and customer profile data. The pipeline supports both local and S3-based input and outputs a unified FactOrders table ready for analytics.

---

## 🚀 Objective

Retail companies often struggle to unify online and in-store sales data alongside CRM records. This project solves that by creating a repeatable, modular pipeline using Python and Pandas that:

- Ingests structured (CSV) and semi-structured (JSON) data
- Cleans and transforms it
- Merges it into a clean star-schema-style model
- Outputs a fact table ready for BI tools

---

## 🗂 Project Structure

```
customer-insights-pipeline/
├── data/                          # Optional for local testing
│   ├── mock_customers.csv
│   ├── mock_store_sales.csv
│   └── mock_online_orders.json
├── outputs/
│   └── fact_orders.csv
    └── fact_orders_from_s3.csv
├── scripts/
│   ├── etl_pipeline.py           # Local file-based ETL
│   └── etl_pipeline_s3.py        # S3-based ETL with boto3
├── requirements.txt
└── .devcontainer/
    └── devcontainer.json
```

---

## 🔧 Tech Stack

- Python 3.10
- Pandas
- Boto3 (for S3 integration)
- JSON & CSV handling
- GitHub Codespaces (DevContainer)

---

## ⚙️ ETL Flow

### Local Version (`etl_pipeline.py`)
1. Load files from `/data`
2. Flatten JSON and clean columns
3. Join with customer master
4. Output to `/outputs/fact_orders.csv`

### S3 Version (`etl_pipeline_s3.py`)
1. Load files from:
   ```
   s3://bashoori-s3/customer-purchase-data/
   ```
2. Transform and join records
3. Save unified dataset to `outputs/fact_orders.csv`

---

## 📄 Output Sample: `fact_orders.csv`

| order_id | customer_id | product_id | quantity | price | timestamp | total_value | region     | customer_segment |
|----------|-------------|------------|----------|--------|-----------|-------------|------------|------------------|
| O2000    | C1001       | P101       | 2        | 59.99  | ...       | 119.98      | East Coast | Silver           |

---

## 🧪 How to Run (S3 Version)

1. Ensure AWS CLI is installed:
   ```bash
   sudo apt install awscli
   ```

2. Configure your credentials:
   ```bash
   aws configure
   ```

3. Run:
   ```bash
   cd scripts
   python etl_pipeline_s3.py
   ```

---

## 📦 Requirements

Install dependencies:
```bash
pip install -r requirements.txt
```

---

## 💻 Dev Environment

Supports GitHub Codespaces with pre-configured Python environment:
```
.devcontainer/devcontainer.json
```

---

## ✍️ Author

**Bita Ashoori**  
_Data Engineer & Data Automation Specialist_  
📎 [GitHub](https://github.com/bashoori) | [LinkedIn](https://www.linkedin.com/in/bashoori)

---

## ⭐️ Show Your Support

If you found this useful, feel free to star the repo or share feedback!


---

## 📥 Data Input Options

This pipeline supports **two modes of input**, allowing it to run both in development (GitHub Codespaces) and production-like (cloud) environments.

### 1. 🟢 S3-Based Input (Cloud Mode)
The script `etl_pipeline_s3.py` reads input files from your AWS S3 bucket:
```
s3://bashoori-s3/customer-purchase-data/
```

Files expected in the bucket:
- `mock_customers.csv`
- `mock_store_sales.csv`
- `mock_online_orders.json`

Run using:
```bash
cd scripts
python etl_pipeline_s3.py
```

### 2. 🧪 Local Input (Development Mode)
The script `etl_pipeline.py` reads files from the local `data/` folder. This is great for GitHub Codespaces or local testing.

Files should be located at:
```
data/
├── mock_customers.csv
├── mock_store_sales.csv
└── mock_online_orders.json
```

Run using:
```bash
cd scripts
python etl_pipeline.py
```

Both scripts output the same result:  
📄 `outputs/fact_orders.csv`

