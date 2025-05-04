from etf_scraper import ETFScraper
from google.oauth2 import service_account
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
import pandas as pd
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

def run_query_nocache(query, _credentials):
    df = pd_gbq.read_gbq(
        query,
        credentials=_credentials)
    return df

def execute_query(query, credentials):
    client = bigquery.Client(
        credentials=credentials,
        project=credentials.project_id,
    )
    try:
        query_job = client.query(query)
        result = query_job.result()
        print(result)
        st.info('Successfully executed query')
    except Exception as e:
        st.error(f'Errors occurred while executing query:\n{e}')
        
def insert_df_to_table(df, dataset_table, credentials):
    client = bigquery.Client(
         credentials=credentials,
         project=credentials.project_id,
    )
    table_id = f'{credentials.project_id}.{dataset_table}'

    client.get_table(table_id)
    print(f"Table {table_id} exists.")

    try:
        # pd_gbq.to_gbq(
        #     df,
        #     table,
        #     if_exists='fail',
        #     credentials=credentials)
        job = client.load_table_from_dataframe(
            df,
            table_id,
            job_config=bigquery.LoadJobConfig(write_disposition="WRITE_APPEND"))
        job.result()  # Wait for the job to finish
        st.info('Successfully inserted df to table')
    except Exception as e:
        st.error(f'Errors occurred while inserting df to table: {table_id}:\n{e}')

def get_ishares_etfs():
    etf_scraper = ETFScraper()
    df = etf_scraper.listings_df
    cols = ['ticker', 'fund_name', 'asset_class', 'subasset_class', 'country', 'region']
    dfs = df.loc[(df.fund_type=='ETF') & (df.provider=='IShares'), cols]
    dfs.rename(columns={'ticker':'symbol'}, inplace=True)
    return dfs


if __name__ == '__main__':
    get_ishares_etfs()

