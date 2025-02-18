import os
import sys
import streamlit as st
import pandas as pd
import plotly.express as px

from config.constants import SECTOR_ETFS

# 🚀 Ensure Python finds 'config' and other modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config.db_utils import get_db_connection

# 🏗️ Page Configuration
st.set_page_config(
    page_title="Stock Market Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🎨 Custom Styling
st.markdown("""
    <style>
        .big-font {font-size:20px !important;}
        .stMarkdown {text-align: center;}
        table { width: 100%; }
    </style>
""", unsafe_allow_html=True)


# 🎯 Fetch Data Functions
def get_live_data(table_name, group_by_col):
    """Fetch the most recent entry per sector or stock from live data tables, removing unwanted columns."""
    conn = get_db_connection()
    query = f"""
        SELECT * FROM {table_name} AS t1
        WHERE datetime = (SELECT MAX(datetime) FROM {table_name} WHERE {group_by_col} = t1.{group_by_col})
    """
    df = pd.read_sql(query, conn)
    conn.close()

    # 🔥 Remove unnecessary columns
    columns_to_remove = ["id", "datetime"]  # ✅ Customize this list
    df = df.drop(columns=[col for col in columns_to_remove if col in df.columns], errors="ignore")

    return df


# ✅ Fetch Live Stock Data with Sector Information
def get_live_stock_data():
    conn = get_db_connection()
    query = """
        SELECT live_stocks.*, stock_metadata.sector
        FROM live_stocks
        JOIN stock_metadata ON live_stocks.ticker = stock_metadata.ticker
    """
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def get_historical_data(ticker):
    """Fetch historical stock data"""
    conn = get_db_connection()
    query = f"SELECT * FROM historical_stocks WHERE ticker = '{ticker}' ORDER BY date DESC LIMIT 500"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


# ✅ Get Sector and Stock Metadata
def get_sector_list():
    """Fetch unique sectors"""
    conn = get_db_connection()
    query = "SELECT DISTINCT sector FROM stock_metadata"
    df = pd.read_sql(query, conn)
    conn.close()
    return df["sector"].dropna().tolist()


def get_stock_metadata():
    """Fetch stock tickers with corresponding sectors"""
    conn = get_db_connection()
    query = "SELECT ticker, sector FROM stock_metadata"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


# 📌 Sidebar Filters
st.sidebar.header("📌 Dashboard Filters")

# 🚀 Get sector and stock data
sectors = get_sector_list()
stock_metadata = get_stock_metadata()

# 🔹 Select a sector (Optional)
selected_sector = st.sidebar.selectbox(
    "📌 Select a Sector (Optional)", ["All Sectors"] + sectors, key="sector_select"
)

# 🔹 Filter stocks based on selected sector
if selected_sector == "All Sectors":
    stock_list = stock_metadata["ticker"].unique().tolist()
else:
    stock_list = stock_metadata[stock_metadata["sector"] == selected_sector]["ticker"].unique().tolist()

# 🔹 Select a stock (Only one dropdown)
selected_stock = st.sidebar.selectbox("📌 Select a Stock", stock_list, key="stock_select")

# 🔹 Choose Data View
view_option = st.sidebar.selectbox("Choose Data View", ["Live Market", "Forecast & Anomaly Detection"], key="view_option")

# 📊 **Left Panel - Sector & Stock Tables**
st.sidebar.subheader("📊 Live Sector Performance")
live_sectors = get_live_data("live_sectors", "sector")  # Fetch only the latest entry per sector
st.sidebar.dataframe(live_sectors)

st.sidebar.subheader("📈 Live Stock Performance")
live_stocks = get_live_stock_data()

# 🔹 Show only latest data per stock
latest_stocks = live_stocks.sort_values(by="datetime", ascending=False).drop_duplicates(subset=["ticker"])
st.sidebar.dataframe(latest_stocks)

# 📈 **Main Panel - Stock Chart & Trading Volume**
st.title(f"📊 {selected_stock} Performance Overview")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Stock Price Movement (30D & 90D MA)")

    stock_data = get_historical_data(selected_stock)
    stock_data["date"] = pd.to_datetime(stock_data["date"])
    stock_data["30D MA"] = stock_data["close_price"].rolling(window=30).mean()
    stock_data["90D MA"] = stock_data["close_price"].rolling(window=90).mean()

    fig_stock = px.line(
        stock_data, x="date", y=["close_price", "30D MA", "90D MA"],
        labels={"date": "Date", "close": "Stock Price"},
        title=f"{selected_stock} Stock Price with Moving Averages",
        template="plotly_dark"
    )
    st.plotly_chart(fig_stock, use_container_width=True)

with col2:
    st.subheader("📊 Trading Volume")

    fig_volume = px.bar(
        stock_data, x="date", y="volume",
        title=f"{selected_stock} Trading Volume",
        labels={"date": "Date", "volume": "Volume"},
        template="plotly_dark"
    )
    st.plotly_chart(fig_volume, use_container_width=True)

# 🚀 Forecasting & Anomaly Detection Panel
if view_option == "Forecast & Anomaly Detection":
    st.title("🔮 Forecasting & Anomaly Detection")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"📈 Forecasted Price for {selected_stock}")

        # 🔥 Placeholder for ML Forecasting Data (To Be Implemented)
        # forecasted_data = get_forecasted_data(selected_stock)
        # fig_forecast = px.line(
        #     forecasted_data, x="date", y="predicted_price",
        #     title=f"{selected_stock} Price Forecast",
        #     labels={"date": "Date", "predicted_price": "Predicted Price"}
        # )
        # st.plotly_chart(fig_forecast, use_container_width=True)

        st.write("⚠️ *Forecasting model not implemented yet. This will display predicted prices.*")

    with col2:
        st.subheader("🚨 Anomaly Detection Alerts")

        # 🔥 Placeholder for ML Anomaly Detection (To Be Implemented)
        # anomalies = get_anomalies(selected_stock)
        # st.dataframe(anomalies)

        st.write("⚠️ *Anomaly detection will highlight unusual market behavior.*")

# 🎯 Final Notes
st.sidebar.markdown("---")
st.sidebar.markdown("📊 **Developed for Live Market Monitoring & Analysis**")
