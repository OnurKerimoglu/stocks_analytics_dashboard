class Queries():
    def __init__(self):
        pass
    
    def distinct_etfs(self):
        query = """
        SELECT DISTINCT(fund_ticker)
        FROM `stocks-455113.stocks_raw.etfs`
        """
        return query
    
    def top_tickers_of_etf(
            self,
            etf_symbol): 
        query = f"""
        SELECT symbol, company_name, weight, sector
        FROM `stocks-455113.stocks_refined_dev.etf_{etf_symbol}_tickers_combined`
        ORDER BY weight_rank ASC
        """
        return query
