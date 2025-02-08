import sqlite3
import config

def create_database():
    """
    Creates the SQLite database and tables if they do not exist.
    """
    conn = sqlite3.connect(config.DB_NAME)
    cursor = conn.cursor()

    # Enable Foreign Key Support
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Create Historical Indexes Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS indexes_historical (
        index_id INTEGER PRIMARY KEY AUTOINCREMENT,
        index_symbol TEXT NOT NULL,
        date DATE NOT NULL,
        open FLOAT,
        high FLOAT,
        low FLOAT,
        close FLOAT,
        volume BIGINT
    );
    """)

    # Create Historical Sectors Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sectors_historical (
        sector_id INTEGER PRIMARY KEY AUTOINCREMENT,
        sector_name TEXT UNIQUE NOT NULL,
        date DATE DEFAULT CURRENT_DATE,  -- Make this optional with default value
        performance_percent FLOAT
    );
    """)

    # Create Historical Stocks Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stocks_historical (
        stock_id INTEGER PRIMARY KEY AUTOINCREMENT,
        stock_symbol TEXT NOT NULL,
        sector_id INTEGER,
        index_id INTEGER,
        date DATE NOT NULL,
        open FLOAT,
        high FLOAT,
        low FLOAT,
        close FLOAT,
        volume BIGINT,
        FOREIGN KEY (sector_id) REFERENCES sectors_historical(sector_id) ON DELETE SET NULL,
        FOREIGN KEY (index_id) REFERENCES indexes_historical(index_id) ON DELETE SET NULL
    );
    """)

    # Create Live Indexes Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS indexes_live (
        index_id INTEGER PRIMARY KEY AUTOINCREMENT,
        index_symbol TEXT NOT NULL,
        open FLOAT,
        high FLOAT,
        low FLOAT,
        close FLOAT,
        volume BIGINT,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Create Live Sectors Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sectors_live (
        sector_id INTEGER PRIMARY KEY AUTOINCREMENT,
        sector_name TEXT NOT NULL,
        performance_percent FLOAT,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Create Live Stocks Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS stocks_live (
        stock_id INTEGER PRIMARY KEY AUTOINCREMENT,
        stock_symbol TEXT NOT NULL,
        sector_id INTEGER,
        index_id INTEGER,
        open FLOAT,
        high FLOAT,
        low FLOAT,
        close FLOAT,
        volume BIGINT,
        last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (sector_id) REFERENCES sectors_historical(sector_id) ON DELETE SET NULL,
        FOREIGN KEY (index_id) REFERENCES indexes_historical(index_id) ON DELETE SET NULL
    );
    """)

    # Commit and close connection
    conn.commit()
    conn.close()
    print(f"✅ SQLite database '{config.DB_NAME}' and tables created successfully!")

if __name__ == "__main__":
    create_database()

