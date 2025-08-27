class Queries():
    def __init__(self, CONFIG):
        self.DWH = CONFIG['DWH']
    
    def etf_info(self):
        table_id_etfs = f"{self.DWH['project']}.{self.DWH['DS_raw']}.{self.DWH['T_etfs']}"
        table_id_info = f"{self.DWH['project']}.{self.DWH['DS_raw']}.{self.DWH['T_info']}"
        query = f"""
        WITH distinct_etfs AS (
        SELECT DISTINCT(fund_ticker) as symbol
        FROM {table_id_etfs}
        )
        SELECT
        i.symbol, i.company_name
        FROM {table_id_info} i
        JOIN distinct_etfs e on e.symbol=i.symbol

        """
        return query
    
    def etf_top_tickers(
            self,
            etf_symbol):
        table_id_combined = f"{self.DWH['project']}.{self.DWH['DS_refined']}.etf_{etf_symbol}_tickers_combined"
        query = f"""
        SELECT weight_rank as rank, symbol, company_name, weight, sector
        FROM {table_id_combined}
        ORDER BY weight_rank ASC
        """
        return query
    
    def etf_sectoral_composition(
            self,
            etf_symbol):
        table_id_aggregates = f"{self.DWH['project']}.{self.DWH['DS_refined']}.etf_{etf_symbol}_sector_aggregates"
        query = f"""
        WITH sums AS (
        SELECT
        sum(summed_weight) as summed_weight
        FROM {table_id_aggregates}
        )
        SELECT
        sector,
        summed_weight / (select summed_weight from sums) * 100 as cumulative_weight
        FROM {table_id_aggregates}
        """
        return query
    
    def etf_bollinger_recs(
            self,
            etf_symbol):
        table_id_combined = f"{self.DWH['project']}.{self.DWH['DS_refined']}.etf_{etf_symbol}_tickers_combined"
        query = f"""
        SELECT
        bollinger_recommendation,
        COUNT(*) AS count
        FROM {table_id_combined}
        GROUP BY
        bollinger_recommendation
        """
        return query
    
    def etf_time_series(
            self,
            etf_symbol):
        table_id_topprices = f"{self.DWH['project']}.{self.DWH['DS_refined']}.etf_{etf_symbol}_top_ticker_prices"
        query = f"""
        SELECT
        symbol,
        date,
        close,
        weight_rank
        FROM {table_id_topprices}
        WHERE
        (
        weight_rank < 12
        ) 
        AND (
        date >= TIMESTAMP_TRUNC(
            TIMESTAMP_ADD(CURRENT_TIMESTAMP(), INTERVAL -90 day),
            day
            )
        )
        AND (
        date < TIMESTAMP_TRUNC(CURRENT_TIMESTAMP(), day)
        )
        """
        return query

    def etf_main_time_series(
            self,
            etf_symbol):
        table_id_prices = f"{self.DWH['project']}.{self.DWH['DS_raw']}.{self.DWH['T_prices']}"
        query = f"""
        SELECT
        date,
        close,
        high,
        low,
        open
        FROM {table_id_prices}
        WHERE
        symbol = '{etf_symbol}'
        AND (
        date >= TIMESTAMP_TRUNC(
            TIMESTAMP_ADD(CURRENT_TIMESTAMP(), INTERVAL -90 day),
            day
            )
        )
        AND (
        date < TIMESTAMP_TRUNC(CURRENT_TIMESTAMP(), day)
        )
        """
        return query

    def etf_forecast(
            self,
            etf_symbol):
        table_id_forecasts = f"{self.DWH['project']}.{self.DWH['DS_refined']}.{self.DWH['T_forecasts_latest']}"
        query = f"""
        SELECT
        Date as date,
        Close as close,
        FROM {table_id_forecasts}
        WHERE
        Ticker = '{etf_symbol}'
        """
        return query
    
    def etf_main_info(
            self,
            etf_symbol):
        table_id_info = f"{self.DWH['project']}.{self.DWH['DS_raw']}.{self.DWH['T_info']}"
        query = f"""
        SELECT
        symbol, company_name, date_fetched
        FROM {table_id_info}
        WHERE
        symbol = '{etf_symbol}'
        """
        return query
    
    def user_etfs(
            self,
            user
        ):
        table_id_etfs = f"{self.DWH['project']}.{self.DWH['DS_user']}.{self.DWH['T_etfs2track']}"
        query=f"""
        SELECT
        symbol, user
        FROM
        {table_id_etfs}
        where user = '{user}'   
        """
        return query
        