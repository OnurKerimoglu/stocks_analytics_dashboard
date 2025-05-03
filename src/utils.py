from etf_scraper import ETFScraper
from google.oauth2 import service_account
import pandas as pd
import streamlit as st


# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    df = pd.read_gbq(query, credentials=credentials)
    return df

def get_ishares_etfs():
    etf_scraper = ETFScraper()
    df = etf_scraper.listings_df
    cols = ['ticker', 'fund_name', 'asset_class', 'subasset_class', 'country', 'region']
    dfs = df.loc[(df.fund_type=='ETF') & (df.provider=='IShares'), cols]
    dfs.rename(columns={'ticker':'symbol'}, inplace=True)
    return dfs


if __name__ == '__main__':
    get_ishares_etfs()

