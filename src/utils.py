from etf_scraper import ETFScraper

def get_ishares_etfs():
    etf_scraper = ETFScraper()
    df = etf_scraper.listings_df
    cols = ['ticker', 'fund_name', 'asset_class', 'subasset_class', 'country', 'region']
    dfs = df.loc[(df.fund_type=='ETF') & (df.provider=='IShares'), cols]
    dfs.rename(columns={'ticker':'symbol'}, inplace=True)
    return dfs

if __name__ == '__main__':
    get_ishares_etfs()

