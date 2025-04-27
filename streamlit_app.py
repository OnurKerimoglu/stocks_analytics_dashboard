from google.oauth2 import service_account
import pandas
from plotly import express as px
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
st.write(
    "Here you can analyze the ETFs you are interested in."
)

distinct_etfs_query = queries.distinct_etfs()
df = run_query(distinct_etfs_query)
etf_symbol = st.selectbox(
        "Choose the ETF to analyze", sorted(list(df.fund_ticker))
    )

if not etf_symbol:
    st.error("Please select at least one ETF")
else:
    st.subheader(f"Top 10 tickers in: ETF: {etf_symbol}")
    top_tickers_query = queries.etf_top_tickers(etf_symbol)
    df = run_query(top_tickers_query)
    st.dataframe(df.sort_index())

    st.subheader(f"Sectoral Composition of ETF: {etf_symbol}")
    sectoral_composition_query = queries.etf_sectoral_composition(etf_symbol)
    df = run_query(sectoral_composition_query)
    fig = px.pie(
        df,
        values='adjusted_total_weight',
        names='sector', 
        # title=f"ETF: {etf_symbol}"
        )
    st.plotly_chart(fig, theme=None)

    st.subheader(f"Bollinger Recommendations for holdings of ETF: {etf_symbol}")
    br_query = queries.etf_bollinger_recs(etf_symbol)
    df = run_query(br_query)
    fig = px.pie(
        df,
        values='count',
        names='bollinger_recommendation', 
        # title=f"ETF: {etf_symbol}"
        )
    st.plotly_chart(fig, theme=None)