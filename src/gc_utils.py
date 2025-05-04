from google.cloud import bigquery
import pandas_gbq as pd_gbq
import streamlit as st


class BQFunctions():
    def __init__(self, CONFIG, credentials):
        self.DWH = CONFIG['DWH']
        self.credentials_admin = credentials

    def run_query_nocache(self, query):
        df = pd_gbq.read_gbq(
            query,
            credentials=self.credentials_admin)
        return df

    def execute_query(self, query):
        client = bigquery.Client(
            credentials=self.credentials_admin,
            project=self.credentials_admin.project_id,
        )
        try:
            query_job = client.query(query)
            result = query_job.result()
            print(result)
            # st.info('Successfully executed query')
        except Exception as e:
            st.error(f'Errors occurred while executing query:\n{e}')
            
    def insert_df_to_table(self, df, dataset_table):
        client = bigquery.Client(
            credentials=self.credentials_admin,
            project=self.credentials_admin.project_id,
        )
        table_id = f"{self.DWH['project']}.{dataset_table}"

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
            # st.info('Successfully inserted df to table')
        except Exception as e:
            st.error(f'Errors occurred while inserting df to table: {table_id}:\n{e}')

