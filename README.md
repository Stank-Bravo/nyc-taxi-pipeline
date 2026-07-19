# 🚕 NYC Yellow Taxi Analytics Pipeline

An end-to-end big data pipeline that processes 2.7M+ NYC taxi trip records using PySpark, with results visualized in an interactive Streamlit dashboard.

---

## 📌 Project Overview

This project demonstrates a complete data engineering workflow:
- **Ingest** raw NYC TLC trip data (Parquet format)
- **Clean** and validate 2.7M+ records using PySpark
- **Transform** raw fields into meaningful features
- **Aggregate** key metrics for analysis
- **Visualize** insights via an interactive dashboard

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| PySpark 3.4.3 | Distributed data processing |
| Python 3.12 | Core language |
| Pandas | Data conversion for dashboard |
| Streamlit | Interactive dashboard |
| Plotly | Charts and visualizations |
| Google Colab | PySpark execution environment |

---

## 📊 Key Findings

- **2,721,041** trips processed after cleaning
- **Peak demand** at 6 PM (195k+ trips in that hour alone)
- **Lowest demand** at 4 AM (~12k trips)
- **Weekday avg fare:** $18.61 vs **Weekend avg fare:** $17.84
- **Weekday trips** are slightly longer in duration (15.3 mins vs 13.6 mins)
- Fare distribution is right-skewed — majority of trips cost under $20

---

## 🔄 Pipeline Architecture
NYC TLC Open Data (Parquet)
↓
PySpark Ingest
↓
Data Cleaning
(null removal, outlier filtering)
↓
Feature Engineering
(pickup_hour, trip_duration, day_type)
↓
Aggregations
(hourly demand, avg fare by day type)
↓
Export to CSV
↓
Streamlit Dashboard

---

## 📁 Project Structure
nyc-taxi-pipeline/
│
├── pipeline.py        # PySpark ingestion, cleaning, transformation
├── dashboard.py       # Streamlit dashboard
├── .gitignore         # Excludes data files
└── README.md

---

## 🚀 How to Run

### 1. Run the Pipeline (Google Colab recommended)
- Upload `yellow_tripdata_2024-01.parquet` from [NYC TLC Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
- Run `pipeline.py` cells in Colab
- Download the 3 output CSVs into `data/`

### 2. Run the Dashboard (local)
```bash
pip install streamlit plotly pandas
streamlit run dashboard.py
```

---

## 📂 Data Source

[NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) — January 2024, Yellow Taxi

---

## 👤 Author

**Chinmay Agrawal**  
B.Tech CS (Big Data Specialization) — NIIT University  
[LinkedIn](https://www.linkedin.com/in/chinmay--agrawal) • [GitHub](https://github.com/Stank-Bravo)
