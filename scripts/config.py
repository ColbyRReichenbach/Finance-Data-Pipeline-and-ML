# config.py

### API CONFIGURATION ###
API_PROVIDER = "yahoo"  # Change this if switching APIs
YAHOO_FINANCE_API_URL = "https://query1.finance.yahoo.com/v8/finance/chart/"
ALTERNATIVE_API_URL = ""  # If switching to another API, set the endpoint here
API_KEY = ""  # Store API key if needed (e.g., for paid providers)

### DATABASE CONFIGURATION ###
DB_NAME = "finance_data.db"

### FINANCIAL SYMBOLS CONFIGURATION ###
INDEX_SYMBOLS = ["^GSPC", "^IXIC", "^DJI"]  # S&P 500, NASDAQ, Dow Jones

SECTOR_NAMES = [
    "Technology",
    "Financial Services",
    "Consumer Cyclical",
    "Healthcare",
    "Communication Services",
    "Industrials",
    "Consumer Defensive",
    "Energy",
    "Real Estate",
    "Basic Materials",
    "Utilities"
]

STOCK_SYMBOLS = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]  # Modify based on needs

### LIVE DATA CONFIGURATION ###
LIVE_UPDATE_INTERVAL = 15  # Update live data every 15 minutes

### FEATURE ENGINEERING CONFIGURATION ###
USE_ENGINEERED_FEATURES = True  # Enable/Disable feature engineering

# STOCK-TO-SECTOR MAPPING (Updated for Yahoo Finance)
STOCK_SECTOR_MAP = {
    "AAPL": "Technology",
    "MSFT": "Technology",
    "GOOGL": "Communication Services",
    "AMZN": "Consumer Cyclical",
    "TSLA": "Consumer Cyclical",
    "JPM": "Financial Services",
    "XOM": "Energy",
    "PG": "Consumer Defensive",
    "VZ": "Communication Services",
    "UNH": "Healthcare"
}

### STOCK-TO-INDEX MAPPING ###
STOCK_INDEX_MAP = {
    "AAPL": "^GSPC",  # S&P 500
    "MSFT": "^GSPC",  # S&P 500
    "GOOGL": "^GSPC",  # S&P 500
    "AMZN": "^IXIC",  # NASDAQ
    "TSLA": "^IXIC",  # NASDAQ
}
