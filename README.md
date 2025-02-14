# Finance Data Pipeline

A Python-based financial data pipeline for fetching, storing, and analyzing **historical & live stock data**.

## Features 
- Fetch **historical** and **live** data from Yahoo Finance.
- Store data in an **SQLite database** for easy analysis.
- **Machine Learning models** for:
  - **Anomaly Detection** (detect unusual stock movements).
  - **Stock Price Prediction** (forecast stock trends).
- Real-time **sector, stock and index analysis**.

---

## Project Structure 📂

```bash
finance-data-pipeline/
│── fetch/                 # Fetch scripts (historical, live, metadata, fundamentals)
│── store/                 # Store scripts for DB insertion
│── analytics/             # Data analysis scripts
│── charts/                # Visualization scripts
│── dashboard/             # Dashboard (Streamlit/Plotly)
│── config/                # Config files (constants, DB paths, etc.)
│── tests/                 # Test scripts for fetch/store functions
│── docs/                  # Documentation (README, guides, etc.)
│── scripts/               # Utility scripts (setup, reset DB, cron jobs, etc.)
│── data/                  # Store sample data files (CSV, JSON, etc.)
│── models/                # ML models (forecasts, anomaly detection)
│── notebooks/             # Jupyter notebooks for exploratory analysis
│── .gitignore             # Ignore unnecessary files
│── requirements.txt       # Required Python libraries
│── setup.py               # Installation setup (if making package)
│── LICENSE                # Open-source or private license
│── README.md              # Project description & setup instructions
│── sql_finance_project.db  # SQLite DB

```
## **Contact Me:**  
Colby Reichenbach  
[colbyrreichenabch@gmail.com](mailto:colbyrreichenbach@gmail.com)  
[Linkedin](https://www.linkedin.com/in/colby-reichenbach/)  

