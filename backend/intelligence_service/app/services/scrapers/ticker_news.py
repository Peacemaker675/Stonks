import yfinance as yf
import logging
from datetime import datetime
from typing import List, Dict

logger = logging.getLogger(__name__)

class TickerNewsScraper:
    def fetch_news(self, ticker_symbol: str) -> List[Dict]:
        """
        Fetches news specifically for a company (e.g., 'RELIANCE.NS')
        """
        try:
            # Handle Indian NSE/BSE suffixes
            if not (ticker_symbol.endswith(".NS") or ticker_symbol.endswith(".BO")):
                ticker_symbol += ".NS"
                
            logger.info(f"Fetching news for {ticker_symbol}...")
            stock = yf.Ticker(ticker_symbol)
            news_list = stock.news
            
            clean_news = []
            for item in news_list:
                # Basic cleaning of YFinance response
                clean_news.append({
                    "title": item.get('title'),
                    "source": item.get('publisher'),
                    "url": item.get('link'),
                    "published_at": datetime.fromtimestamp(item.get('providerPublishTime', 0)).isoformat(),
                    "related_tickers": item.get('relatedTickers', [])
                })
            
            return clean_news
            
        except Exception as e:
            logger.error(f"Error fetching ticker news for {ticker_symbol}: {e}")
            return []