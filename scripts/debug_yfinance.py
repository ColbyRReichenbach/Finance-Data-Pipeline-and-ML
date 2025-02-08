import yfinance as yf
import config

# Select one symbol from the index list for testing
sample_symbol = config.INDEX_SYMBOLS[0]

# Fetch data
stock = yf.Ticker(sample_symbol)
data = stock.history(period="1mo")  # Fetch last month's data

# Print first few rows and available columns
print(f"✅ Sample Data for {sample_symbol}:")
print(data.head())
print("\n📊 Available Columns:")
print(data.columns)
