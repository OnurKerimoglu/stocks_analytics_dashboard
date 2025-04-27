from google.oauth2 import service_account
# from google.cloud import bigquery
import pandas
import streamlit as st

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
#client = bigquery.Client(credentials=credentials)

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    df = pandas.read_gbq(query, credentials=credentials)
    return df

# Print results.
st.title("Stocks-Analytics")
st.write(
    "Here you can find the analytics of the stocks you are interested in."
)

st.subheader("Top 10 tickers in: ETF: IVV")
top_10_tickers_query = """
    SELECT symbol, company_name, weight, sector
    FROM `stocks-455113.stocks_refined_dev.etf_IVV_tickers_combined`
    ORDER BY weight_rank ASC
    """
df = run_query(top_10_tickers_query)
st.dataframe(df.sort_index())

