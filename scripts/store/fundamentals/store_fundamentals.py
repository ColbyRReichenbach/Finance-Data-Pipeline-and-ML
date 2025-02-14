import sqlite3
from config.db_utils import DB_PATH

def store_fundamentals(fundamental_data):
    """Stores stock fundamentals into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO stock_fundamentals (
        ticker, date, market_cap, pe_ratio, price_to_book, beta, total_revenue,
        earnings_growth, revenue_growth, debt_to_equity, return_on_assets,
        return_on_equity, short_ratio, shares_short
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """

    cursor.executemany(insert_query, [
        (
            data["ticker"], data["date"], data["market_cap"], data["pe_ratio"],
            data["price_to_book"], data["beta"], data["total_revenue"],
            data["earnings_growth"], data["revenue_growth"], data["debt_to_equity"],
            data["return_on_assets"], data["return_on_equity"], data["short_ratio"],
            data["shares_short"]
        ) for data in fundamental_data
    ])

    conn.commit()
    conn.close()
    print("✅ Stock fundamentals stored successfully!")

if __name__ == "__main__":
    print("⚠️  Run `fetch_fundamentals.py` instead.")
