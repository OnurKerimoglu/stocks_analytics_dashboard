from google.oauth2 import service_account
import pandas
from plotly import express as px
from plotly import graph_objects as go
import streamlit as st

from src.queries import Queries

queries = Queries()

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    df = pandas.read_gbq(query, credentials=credentials)
    return df

# Print results.
st.title("Stocks-Analytics")

etfs_query = queries.etf_info()
df = run_query(etfs_query)
df["symbol_name"] = df.symbol + " (" + df.company_name + ")"
symbol_name = st.selectbox(
        "Choose the ETF to analyze", sorted(df.symbol_name)
    )
etf_symbol = df[df.symbol_name == symbol_name].symbol.values[0]

if not etf_symbol:
    st.error("Please select at least one ETF")
else:

    st.subheader(f"90 days history (ETF: {etf_symbol})")
    etf_ts_query = queries.etf_main_time_series(etf_symbol)
    df = run_query(etf_ts_query)
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df['date'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close']
                )
            ]
        )
    st.plotly_chart(fig, theme=None)

    st.subheader(f"90 days history of top holdings (ETF: {etf_symbol})")
    etf_ts_query = queries.etf_time_series(etf_symbol)
    df = run_query(etf_ts_query)
    fig = px.line(
        df,
        x="date",
        y="close",
        color="symbol")
    st.plotly_chart(fig, theme=None)
    
    st.subheader(f"Holding weights (ETF: {etf_symbol})")
    top_tickers_query = queries.etf_top_tickers(etf_symbol)
    df = run_query(top_tickers_query)
    df.set_index("rank", inplace=True)
    st.dataframe(df.sort_index())

    st.subheader(f"Sectoral Composition (ETF: {etf_symbol})")
    sectoral_composition_query = queries.etf_sectoral_composition(etf_symbol)
    df = run_query(sectoral_composition_query)
    fig = px.pie(
        df,
        values='cumulative_weight',
        names='sector', 
        # title=f"ETF: {etf_symbol}"
        )
    st.plotly_chart(fig, theme=None)

    st.subheader(f"Bollinger Recommendations for holdings (ETF: {etf_symbol})")
    br_query = queries.etf_bollinger_recs(etf_symbol)
    df = run_query(br_query)
    fig = px.pie(
        df,
        values='count',
        names='bollinger_recommendation', 
        # title=f"ETF: {etf_symbol}"
        )
    st.plotly_chart(fig, theme=None)

