from store.live.store_live_stocks import store_live_stock_data
from store.live.store_live_indexes import store_live_index_data
from store.live.store_live_sectors import store_live_sector_data
from store.fundamentals.store_fundamentals import store_fundamentals

def store_all(live_stocks, live_indexes, live_sectors, fundamentals):
    """Stores all live & fundamental data."""
    print("💾 Storing live stock data...")
    store_live_stock_data(live_stocks)

    print("💾 Storing live index data...")
    store_live_index_data(live_indexes)

    print("💾 Storing live sector data...")
    store_live_sector_data(live_sectors)

    print("💾 Storing fundamentals data...")
    store_fundamentals(fundamentals)

    print("✅ Storing complete!")

