# Finance Data Pipeline

A Python-based financial data pipeline for fetching, storing, and analyzing **historical & live stock data**.

## Features 
- Fetch **historical** and **live** stock data from Yahoo Finance.
- Store data in an **SQLite database** for easy analysis.
- **Machine Learning models** for:
  - **Anomaly Detection** (detect unusual stock movements).
  - **Stock Price Prediction** (forecast stock trends).
- Real-time **sector and index analysis**.

---

## Project Structure 📂

```bash
finance-data-pipeline/
├── fetch/                    # Data fetching scripts
│   ├── fetch_historical_data.py  # Fetch historical stock data
│   ├── fetch_live_data.py        # Fetch live stock data
├── store/                    # Data storage scripts
│   ├── store_historical_data.py  # Store historical stock data
│   ├── store_live_data.py        # Store live stock data
├── ml_models/                # Machine Learning models
│   ├── anomaly_detection.py      # Detect stock anomalies
│   ├── stock_prediction.py       # Predict stock prices
├── scripts/                  # Utility scripts
│   ├── setup_database.py         # Create the SQLite database
│   ├── run_historical_data.py    # Run historical data pipeline
│   ├── run_live_data.py          # Run live data pipeline
├── config.py                  # Config settings (API keys, database paths)
├── requirements.txt            # Python dependencies
├── .gitignore                  # Ignore unnecessary files
├── README.md                   # Project documentation
```
## **Contact Me:**
Colby Reichenbach
[colbyrreichenabch@gmail.com](mailto:colbyrreichenbach@gmail.com)
[Linkedin](https://www.linkedin.com/in/colby-reichenbach/)

