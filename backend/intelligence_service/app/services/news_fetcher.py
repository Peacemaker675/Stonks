from typing import List, Dict
from .scrapers.universal_feed import UniversalNewsScraper
from .scrapers.ticker_news import TickerNewsScraper

class NewsAggregator:
    def __init__(self):
        self.universal_scraper = UniversalNewsScraper()
        self.ticker_scraper = TickerNewsScraper()

    def get_macro_market_news(self) -> List[Dict]:
        """
        Gets broad market news. Used for Regime Detection (Bear/Bull).
        """
        return self.universal_scraper.run()

    def get_stock_specific_news(self, tickers: List[str]) -> Dict[str, List[Dict]]:
        """
        Gets news for your specific stocks.
        Returns: {'RELIANCE': [news_items], 'TCS': [news_items]}
        """
        results = {}
        for ticker in tickers:
            results[ticker] = self.ticker_scraper.fetch_news(ticker)
        return results

    def get_combined_sentiment_data(self, tickers: List[str] = None) -> List[Dict]:
        """
        Helper to get EVERYTHING in one flat list for sentiment analysis.
        """
        all_news = self.get_macro_market_news()
        
        if tickers:
            stock_news_map = self.get_stock_specific_news(tickers)
            for symbol, items in stock_news_map.items():
                all_news.extend(items)
                
        return all_news