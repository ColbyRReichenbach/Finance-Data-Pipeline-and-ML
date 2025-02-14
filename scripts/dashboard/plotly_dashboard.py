import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd
from config.db_utils import get_db_connection

# Initialize Dash App
app = dash.Dash(__name__)


# Fetch data from DB
def fetch_live_stock_data():
    conn = get_db_connection()
    query = "SELECT * FROM live_stocks ORDER BY datetime DESC LIMIT 100"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


# Fetch Historical Data
def fetch_historical_stock_data():
    conn = get_db_connection()
    query = "SELECT * FROM historical_stocks WHERE date >= date('now', '-1 year')"
    df = pd.read_sql(query, conn)
    conn.close()
    return df


# Layout
app.layout = html.Div(children=[
    html.H1("📈 Live Financial Dashboard", style={'textAlign': 'center'}),

    # Dropdowns for Stock Selection
    html.Div([
        html.Label("Select Stock:"),
        dcc.Dropdown(
            id='stock-dropdown',
            options=[
                {'label': 'Apple (AAPL)', 'value': 'AAPL'},
                {'label': 'Microsoft (MSFT)', 'value': 'MSFT'},
                {'label': 'Google (GOOGL)', 'value': 'GOOGL'}
            ],
            value='AAPL'
        )
    ], style={'width': '50%', 'margin': 'auto'}),

    # Live Stock Price Chart
    dcc.Graph(id='live-stock-chart'),

    # Historical Stock Overlay
    dcc.Graph(id='historical-stock-chart'),

    # Forecasting Chart
    dcc.Graph(id='forecast-chart')
])


# Callbacks
@app.callback(
    Output('live-stock-chart', 'figure'),
    Input('stock-dropdown', 'value')
)
def update_live_stock_chart(selected_stock):
    df = fetch_live_stock_data()
    df = df[df['ticker'] == selected_stock]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['datetime'], y=df['close'],
                             mode='lines', name='Live Price'))
    fig.update_layout(title=f"{selected_stock} - Live Stock Prices",
                      xaxis_title="Time",
                      yaxis_title="Price")
    return fig


@app.callback(
    Output('historical-stock-chart', 'figure'),
    Input('stock-dropdown', 'value')
)
def update_historical_chart(selected_stock):
    df = fetch_historical_stock_data()
    df = df[df['ticker'] == selected_stock]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y=df['close'],
                             mode='lines', name='Historical Avg'))
    fig.update_layout(title=f"{selected_stock} - Historical Performance",
                      xaxis_title="Time",
                      yaxis_title="Price")
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
