import sqlite3
from config.db_utils import DB_PATH

def create_tables():
    """Creates all required tables in the database if they do not exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ✅ **Historical Stock Data**
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historical_stocks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT NOT NULL,
        date TEXT NOT NULL,
        open_price REAL,
        close_price REAL,
        high_price REAL,
        low_price REAL,
        volume INTEGER
    );
    """)

    # ✅ **Historical Index Data**
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historical_indexes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        date TEXT NOT NULL,
        open_price REAL,
        close_price REAL,
        high_price REAL,
        low_price REAL,
        volume INTEGER
    );
    """)

    # ✅ **Historical Sector Data**
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS historical_sectors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sector TEXT NOT NULL,
        date TEXT NOT NULL,
        open_price REAL,
        close_price REAL,
        high_price REAL,
        low_price REAL,
        volume INTEGER
    );
    """)

    # ✅ **Live Stock Data**
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS live_stocks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT NOT NULL,
        datetime TEXT NOT NULL,
        open_price REAL,
        close_price REAL,
        high_price REAL,
        low_price REAL,
        volume INTEGER
    );
    """)

    # ✅ **Live Index Data**
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS live_indexes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        symbol TEXT NOT NULL,
        datetime TEXT NOT NULL,
        open_price REAL,
        close_price REAL,
        high_price REAL,
        low_price REAL,
        volume INTEGER
    );
    """)

    # ✅ **Live Sector Data**
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS live_sectors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sector TEXT NOT NULL,
        datetime TEXT NOT NULL,
        open_price REAL,
        close_price REAL,
        high_price REAL,
        low_price REAL,
        volume INTEGER
    );
    """)

    # ✅ Static Company Metadata Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_metadata (
        ticker TEXT PRIMARY KEY,
        company_name TEXT,
        sector TEXT,
        industry TEXT,
        industry_key TEXT,
        website TEXT,
        headquarters TEXT,
        country TEXT,
        full_time_employees INTEGER,
        market_cap BIGINT,
        beta REAL,
        pe_ratio REAL,
        price_to_book REAL,
        dividend_yield REAL,
        dividend_rate REAL,
        payout_ratio REAL,
        earnings_growth REAL,
        revenue_growth REAL,
        debt_to_equity REAL,
        return_on_assets REAL,
        return_on_equity REAL,
        total_cash BIGINT,
        total_debt BIGINT,
        operating_cashflow BIGINT,
        free_cashflow BIGINT,
        profit_margins REAL,
        enterprise_value BIGINT,
        revenue_per_share REAL,
        currency TEXT,
        last_fiscal_year_end TEXT,
        most_recent_quarter TEXT,
        exchange TEXT,
        first_trade_date TEXT,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # ✅ **Stock Fundamentals**
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_fundamentals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT NOT NULL,
        date TEXT NOT NULL,
        market_cap BIGINT,
        pe_ratio REAL,
        price_to_book REAL,
        beta REAL,
        total_revenue BIGINT,
        earnings_growth REAL,
        revenue_growth REAL,
        debt_to_equity REAL,
        return_on_assets REAL,
        return_on_equity REAL,
        short_ratio REAL,
        shares_short BIGINT,
        FOREIGN KEY (ticker) REFERENCES stock_metadata(ticker)
    );
    """)

    # ✅ **ML Anomaly Detections**
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_anomalies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT NOT NULL,
        date TEXT NOT NULL,
        close_price REAL,
        volume INTEGER,
        RSI REAL,
        volatility REAL,
        anomaly INTEGER,
        detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # ✅ **ML Stock Forecasts**
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stock_forecasts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT NOT NULL,
        date TEXT NOT NULL,
        predicted_price REAL,
        model_type TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    conn.commit()
    conn.close()
    print("✅ Database tables created successfully!")

if __name__ == "__main__":
    create_tables()
