# Customer Insights Pipeline

Transform raw customer and transaction data into actionable customer segments and behavioral insights for targeted marketing and retention strategies.

## Overview

Retail and e-commerce businesses have customer data scattered across systems—CRM, transaction databases, website events—but lack a unified view of who their customers are and how they behave. This pipeline consolidates that fragmented data into clean, analysis-ready customer profiles.

**Key Topics**
- Customer data integration from multiple sources
- RFM analysis (Recency, Frequency, Monetary)
- Customer segmentation and clustering
- Behavioral insights for marketing
- Time-series customer activity tracking

## The Problem

A retailer has:
- Customer profiles in CRM (demographics, registration date)
- Transaction history in a data warehouse (orders, amounts, dates)
- Online behavior in event logs (browsing, clicks, abandoned carts)

**Without integration**, each system tells a different story. With integration, you answer:
- Which customers are most valuable?
- Who's at risk of churning?
- Which segments respond to discounts?
- What drives repeat purchases?

## Architecture

### Data Sources
1. **Customer Master** (CSV) — demographics, registration, segment flags
2. **Store Sales** (CSV) — in-store transactions, amounts, dates
3. **Online Orders** (JSON) — e-commerce orders, timestamps, items

### Processing Layers

**Raw Layer**
- Ingest all sources as-is
- Preserve load timestamps
- No transformation

**Staging Layer**
- Deduplicate customers (same person across CRM + online)
- Normalize transaction dates and amounts
- Flatten nested JSON structures
- Enforce data types

**Analytics Layer**
- Build customer 360 view (all interactions, one record per customer)
- Calculate RFM metrics (recency, frequency, total spending)
- Flag churn risk (no purchase in 90 days)
- Assign segment (high-value, at-risk, dormant, etc.)

### Output
- **Fact Orders**: Every transaction with customer enrichment
- **Customer Segments**: One row per customer with RFM scores and segment assignment

## Key Design Decisions

### 1. Why RFM?
RFM is simple, interpretable, and proven.
- **Recency**: How recently did customer purchase? (recent = more engaged)
- **Frequency**: How often do they buy? (frequent = loyal)
- **Monetary**: How much do they spend? (high spend = valuable)

Score each 1–5 (5 = best), combine into segments (555 = best, 111 = worst).

### 2. Customer Deduplication
Same customer appears in CRM, online, and store systems under slightly different names/emails.
- Match on email first (exact)
- Match on fuzzy name + phone if email missing
- Create customer_id that links all records
- Track which source is "primary" (most complete)

### 3. Churn Definition
"At-risk" = no purchase in last 90 days (configurable).
- Flag these customers for retention campaigns
- Track their propensity to return
- Measure campaign success by comparing pre/post purchase rates

### 4. Incremental Processing (Optional)
Pipeline can run daily, processing only new/changed data.
- Initial run: backfill all history
- Daily: process new orders, update customer RFM
- Cheaper than full reload, essential at scale

## Project Structure

```
customer-insights-pipeline/
├── data/
│   ├── mock_customers.csv
│   ├── mock_store_sales.csv
│   └── mock_online_orders.json
├── scripts/
│   ├── etl_pipeline.py           # Local processing
│   ├── etl_pipeline_s3.py        # S3-based processing
│   └── sql/
│       └── customer_segments.sql # Optional SQL version
├── outputs/
│   ├── fact_orders.csv
│   └── customer_segments.csv
├── requirements.txt
└── README.md
```

## Running It

### Local
```bash
pip install -r requirements.txt
python scripts/etl_pipeline.py
# Outputs: outputs/fact_orders.csv, outputs/customer_segments.csv
```

### S3-Based
```bash
# Upload raw data to S3
aws s3 cp data/ s3://your-bucket/raw/

# Run pipeline (reads from S3, writes to S3)
python scripts/etl_pipeline_s3.py

# Download results
aws s3 cp s3://your-bucket/analytics/ outputs/
```

## Sample Outputs

### Customer Segments
| customer_id | rfm_score | segment | last_purchase | total_spent | purchase_count |
|---|---|---|---|---|---|
| C001 | 555 | Champion | 2 days ago | $5,200 | 47 |
| C002 | 542 | Loyal High-Value | 15 days ago | $4,100 | 32 |
| C003 | 234 | At-Risk | 120 days ago | $800 | 8 |
| C004 | 111 | Lost | 380 days ago | $150 | 2 |

### Key Insights
- **20% of customers** are Champions (high recency, frequency, monetary)
- **15% at risk** (no purchase in 90+ days)
- **Average spend**: $2,400 (varies 10x across segments)
- **Churn rate**: 5% annually (track by segment)

## What This Demonstrates

**Data Integration Thinking**
- Combined multiple sources (CRM, transactions, events)
- Handled different schemas and formats
- Built a single customer view

**Analytics Capability**
- Designed metrics that drive business decisions
- Translated raw data into actionable segments
- Enabled marketing team to target campaigns

**Python/Data Skills**
- Data wrangling (pandas, deduplication, joins)
- JSON parsing and flattening
- CSV I/O and data validation

## What I'd Do Differently

1. **Use dbt** instead of Python scripts — more testable, versionable, easier to modify
2. **Time-series tracking** — store RFM scores over time, measure segment drift
3. **Lookalike modeling** — use Champions to find similar prospects (ML angle)
4. **Incremental processing** — merge-only-new-data for scale
5. **Data quality framework** — track missing values, outliers, duplicates over time

## Next Steps

- Add predictive churn model (logistic regression)
- Build Lookalike audience from Champions
- Real-time segment assignment (event-driven updates)
- Customer lifetime value (CLV) prediction
- Cohort analysis (compare behavior by acquisition date)

---

**The point:** This pipeline shows how raw customer data becomes a strategic asset—enabling personalization, retention, and growth. That's data engineering with business impact.
