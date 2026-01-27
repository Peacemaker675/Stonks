import feedparser
import trafilatura
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UniversalNewsScraper:
    FEEDS = {
        "moneycontrol_business": "https://www.moneycontrol.com/rss/business.xml",
        "moneycontrol_markets": "https://www.moneycontrol.com/rss/MCtopnews.xml",
        "economic_times": "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms",
        "reuters_business": "https://feeds.reuters.com/reuters/businessNews",
        "investing_com": "https://www.investing.com/rss/stock.rss"
    }

    def _fetch_article_body(self, url: str) -> Optional[Dict]:
        try:
            downloaded = trafilatura.fetch_url(url)
            if downloaded is None:
                return None
                
            result = trafilatura.extract(
                downloaded, 
                include_comments=False, 
                include_tables=False, 
                no_fallback=True,
                output_format='json',
                date_extraction_params={'extensive_search': True}
            )
            
            if result:
                import json
                data = json.loads(result)
                return {
                    "text": data.get('text'),
                    "date": data.get('date'),
                    "author": data.get('author')
                }
            return None
        except Exception as e:
            logger.warning(f"Failed to extract content from {url}: {e}")
            return None

    def scrape_feed(self, source_name: str, feed_url: str, limit: int = 5) -> List[Dict]:
        logger.info(f"Polling {source_name}")
        try:
            feed = feedparser.parse(feed_url)
        except Exception as e:
            logger.error(f"Failed to parse RSS {source_name}: {e}")
            return []

        articles = []

        for entry in feed.entries[:limit]:
            try:
                article = {
                    "title": entry.title,
                    "url": entry.link,
                    "source": source_name,
                    "published_at": entry.get("published", datetime.now().isoformat()),
                    "summary": entry.get("summary", ""),
                    "full_text": None 
                }

                content_data = self._fetch_article_body(entry.link)
                
                if content_data:
                    article["full_text"] = content_data["text"]
                    # If RSS didn't have a date, use the one from the page
                    if not article["published_at"] and content_data["date"]:
                        article["published_at"] = content_data["date"]
                
                articles.append(article)
                
            except Exception as e:
                logger.error(f"Error processing item in {source_name}: {e}")
                continue

        return articles

    def run(self) -> List[Dict]:
        all_news = []
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = {
                executor.submit(self.scrape_feed, name, url): name 
                for name, url in self.FEEDS.items()
            }
            
            for future in futures:
                try:
                    result = future.result()
                    all_news.extend(result)
                except Exception as e:
                    logger.error(f"Feed scraper thread failed: {e}")
                    
        return all_news