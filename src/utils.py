from etf_scraper import ETFScraper
from google.oauth2 import service_account
import pandas_gbq as pd_gbq
import streamlit as st

credentials_viewer = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account_viewer"])

# Perform read query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    df = pd_gbq.read_gbq(
        query,
        credentials=credentials_viewer)
    return df

def get_ishares_etfs():
    etf_scraper = ETFScraper()
    df = etf_scraper.listings_df
    cols = ['ticker', 'fund_name', 'asset_class', 'subasset_class', 'country', 'region']
    dfs = df.loc[(df.fund_type=='ETF') & (df.provider=='IShares'), cols]
    dfs.rename(columns={'ticker':'symbol'}, inplace=True)
    return dfs

def get_etf_holdings(fund_ticker):
    etf_scraper = ETFScraper()
    df = etf_scraper.query_holdings(fund_ticker, None)
    return df

if __name__ == '__main__':
    get_ishares_etfs()

