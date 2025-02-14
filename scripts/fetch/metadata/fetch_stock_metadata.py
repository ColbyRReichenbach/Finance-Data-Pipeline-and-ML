import yfinance as yf
import pandas as pd
from config.constants import STOCK_TICKERS
from config.db_utils import get_db_connection


def fetch_stock_metadata(ticker):
    """Fetch static metadata for a stock from Yahoo Finance."""
    stock = yf.Ticker(ticker)
    info = stock.info  # Extract metadata

    # Handle missing data gracefully
    metadata = {
        "ticker": ticker,
        "company_name": info.get("longName", "N/A"),
        "sector": info.get("sector", "N/A"),
        "industry": info.get("industry", "N/A"),
        "industry_key": info.get("industryKey", "N/A"),
        "website": info.get("website", "N/A"),
        "headquarters": f"{info.get('city', 'N/A')}, {info.get('state', 'N/A')}, {info.get('country', 'N/A')}",
        "country": info.get("country", "N/A"),
        "full_time_employees": info.get("fullTimeEmployees", 0),
        "market_cap": info.get("marketCap", 0),
        "beta": info.get("beta", 0.0),
        "pe_ratio": info.get("trailingPE", 0.0),
        "price_to_book": info.get("priceToBook", 0.0),
        "dividend_yield": info.get("dividendYield", 0.0),
        "dividend_rate": info.get("dividendRate", 0.0),
        "payout_ratio": info.get("payoutRatio", 0.0),
        "earnings_growth": info.get("earningsGrowth", 0.0),
        "revenue_growth": info.get("revenueGrowth", 0.0),
        "debt_to_equity": info.get("debtToEquity", 0.0),
        "return_on_assets": info.get("returnOnAssets", 0.0),
        "return_on_equity": info.get("returnOnEquity", 0.0),
        "total_cash": info.get("totalCash", 0),
        "total_debt": info.get("totalDebt", 0),
        "operating_cashflow": info.get("operatingCashflow", 0),
        "free_cashflow": info.get("freeCashflow", 0),
        "profit_margins": info.get("profitMargins", 0.0),
        "enterprise_value": info.get("enterpriseValue", 0),
        "revenue_per_share": info.get("revenuePerShare", 0.0),
        "currency": info.get("financialCurrency", "N/A"),
        "last_fiscal_year_end": info.get("lastFiscalYearEnd", "N/A"),
        "most_recent_quarter": info.get("mostRecentQuarter", "N/A"),
        "exchange": info.get("exchange", "N/A"),
        "first_trade_date": info.get("firstTradeDateEpochUtc", "N/A")
    }

    return metadata


def fetch_and_store_stock_metadata():
    """Fetch and store metadata for all stocks in bulk."""
    all_data = []

    for ticker in STOCK_TICKERS:
        metadata = fetch_stock_metadata(ticker)
        all_data.append(metadata)

    if all_data:
        df = pd.DataFrame(all_data)

        # ✅ Ensure column names match the database schema
        conn = get_db_connection()
        df.to_sql("stock_metadata", conn, if_exists="replace", index=False)
        conn.close()

        print(f"✅ Successfully stored metadata for {len(STOCK_TICKERS)} stocks!")


if __name__ == "__main__":
    fetch_and_store_stock_metadata()
