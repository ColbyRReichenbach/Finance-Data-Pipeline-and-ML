import os

# STOCK SYMBOLS
STOCK_TICKERS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

# MARKET INDEX SYMBOLS
INDEX_TICKERS = ["^GSPC", "^IXIC", "^DJI"]

# SECTOR ETFs (Represents Each Sector)
SECTOR_ETFS = {
    "Technology": "XLK",
    "Health Care": "XLV",
    "Financials": "XLF",
    "Consumer Discretionary": "XLY",
    "Communication Services": "XLC",
    "Industrials": "XLI",
    "Consumer Staples": "XLP",
    "Energy": "XLE",
    "Utilities": "XLU",
    "Real Estate": "XLRE",
    "Materials": "XLB"
}

# Ensure the database always resides in the main project directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "finance_data.db")

# HISTORICAL DATA SETTINGS
HISTORICAL_START = "2000-01-01"

# LIVE FETCH SETTINGS
LIVE_INTERVAL = 900  # Fetch every 15 minutes (900 seconds)

FUNDAMENTAL_INTERVAL = "daily"
