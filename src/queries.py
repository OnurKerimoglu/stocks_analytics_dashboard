class Queries():
    def __init__(self):
        pass
    
    def distinct_etfs(self):
        query = """
        SELECT DISTINCT(fund_ticker)
        FROM `stocks-455113.stocks_raw.etfs`
        """
        return query
    
    def etf_top_tickers(
            self,
            etf_symbol): 
        query = f"""
        SELECT symbol, company_name, weight, sector
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
        summed_weight / (select summed_weight from sums) * 100 as adjusted_total_weight
        FROM
        stocks_refined_dev.etf_{etf_symbol}_sector_aggregates
        """
        return query
