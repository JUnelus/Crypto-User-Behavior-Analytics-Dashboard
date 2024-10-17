import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
from db_connection import engine  # Import the engine from db_connection.py


# Load data from PostgreSQL
def load_data():
    df = pd.read_sql('SELECT * FROM onchain_data', engine)
    return df


# Create a Dash app
app = dash.Dash(__name__)

# Load data for visualization
df = load_data()

# Create a bar chart with descriptions as hover data
app.layout = html.Div(children=[
    html.H1(children='Ethereum Address Balances'),

    dcc.Graph(
        id='eth-balances-graph',
        figure=px.bar(
            df,
            x='balance',
            y='address',
            orientation='h',
            title='Balances of Ethereum Addresses',
            labels={'address': 'Ethereum Address', 'balance': 'ETH Balance'},
            color='balance',
            color_continuous_scale=px.colors.sequential.Viridis,
            hover_data=['description']  # Include the description in the hover data
        )
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
