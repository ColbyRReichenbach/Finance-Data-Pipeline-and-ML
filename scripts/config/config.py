import os

# Load environment variables from .env file
# load_dotenv()
# API Provider
API_PROVIDER = "yahoo"
ALTERNATIVE_PROVIDER = ""
YAHOO_FINANCE_API_URL = "https://query1.finance.yahoo.com/v8/finance/chart/"
ALTERNATIVE_API_URL = ""

# API KEYS (if needed in the future)
YFINANCE_API_KEY = os.getenv("YFINANCE_API_KEY", "")
ALTERNATIVE_API_KEY = ""
# DEBUG MODE (Useful for development)
DEBUG = True
