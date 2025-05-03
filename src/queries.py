class Queries():
    def __init__(self):
        pass
    
    def etf_info(self):
        query = """
        WITH distinct_etfs AS (
        SELECT DISTINCT(fund_ticker) as symbol
        FROM `stocks-455113.stocks_raw_dev.etfs`
        )
        SELECT
        i.symbol, i.company_name
        FROM stocks_raw_dev.stock_info i
        JOIN distinct_etfs e on e.symbol=i.symbol

        """
        return query
    
    def etf_top_tickers(
            self,
            etf_symbol): 
        query = f"""
        SELECT weight_rank as rank, symbol, company_name, weight, sector
        FROM `stocks-455113.stocks_refined_dev.etf_{etf_symbol}_tickers_combined`
        ORDER BY weight_rank ASC
        """
        return query
    
    def etf_sectoral_composition(
            self,
            etf_symbol):
        query = f"""
        WITH sums AS (
        SELECT
        sum(summed_weight) as summed_weight
        FROM
        stocks_refined_dev.etf_{etf_symbol}_sector_aggregates
        )
        SELECT
        sector,
        summed_weight / (select summed_weight from sums) * 100 as cumulative_weight
        FROM
        stocks_refined_dev.etf_{etf_symbol}_sector_aggregates
        """
        return query
    
    def etf_bollinger_recs(
            self,
            etf_symbol):
        query = f"""
        SELECT
        bollinger_recommendation,
        COUNT(*) AS count
        FROM
        stocks_refined_dev.etf_{etf_symbol}_tickers_combined
        GROUP BY
        bollinger_recommendation
        """
        return query
    
    def etf_time_series(
            self,
            etf_symbol):
        query = f"""
        SELECT
        symbol,
        date,
        close,
        weight_rank
        FROM
        stocks_refined_dev.etf_{etf_symbol}_top_ticker_prices
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
        query = f"""
        SELECT
        date,
        close,
        high,
        low,
        open
        FROM
        stocks_raw_dev.stock_prices
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
    
    def etf_main_info(
            self,
            etf_symbol):
        query = f"""
        SELECT
        symbol, company_name, date_fetched
        FROM
        stocks_raw_dev.stock_info
        WHERE
        symbol = '{etf_symbol}'
        """
        return query
    
    def user_etfs(
            self,
            user
        ):
        query="""
        SELECT
        symbol
        FROM
        stocks_user_data.ETFS_to_track
        where user = '{user}'   
        """
        return query