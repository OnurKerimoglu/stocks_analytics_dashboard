from google.oauth2 import service_account
import pandas
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
        "Choose the ETF to analyze", list(df.fund_ticker)
    )

if not etf_symbol:
    st.error("Please select at least one country.")
else:
    st.subheader(f"Top 10 tickers in: ETF: {etf_symbol}")
    top_tickers_query = queries.top_tickers_of_etf(etf_symbol)
    df = run_query(top_tickers_query)
    st.dataframe(df.sort_index())

