from fastapi import APIRouter, Depends, HTTPException
import yfinance
from app.services.news_fetcher import NewsAggregator
from app.ml_engine.sentiment_analyzer import SentimentEngine
from app.ml_engine.regime_detector import RegimeDetector
from app.schemas.payloads import RegimeSignal

router = APIRouter()
sentiment_engine = SentimentEngine()
regime_detector = RegimeDetector()
news_aggregator = NewsAggregator() # Assumes you saved the scraper code from previous turn

@router.get("/refresh-intelligence", response_model=RegimeSignal)
async def refresh_market_intelligence():
    """
    Main heartbeat: Scrapes news -> Analyzes Sentiment -> Determines Regime
    """
    # 1. Fetch News
    articles = news_aggregator.get_macro_market_news()
    if not articles:
        raise HTTPException(status_code=503, detail="News source unavailable")
    
    # 2. Calculate Aggregate Sentiment
    total_score = 0
    for article in articles:
        # Use full text if available, else title
        text = article.get('full_text') or article.get('title')
        total_score += sentiment_engine.analyze(text)
    
    avg_sentiment = total_score / len(articles) if articles else 0
    
    # 3. Detect Regime
    vix = yfinance.Ticker("INDIAVIX.NS")
    data = vix.history(period='1d')
    current_vix = 15 # avg value if data is empty
    if not data.empty:
        current_vix = data['Close'].iloc[-1]
    round(current_vix)
    current_vix /= 10 # 25 => 2.5 making it between 0-3 
    decision = regime_detector.detect_regime(market_volatility=current_vix, sentiment_score=avg_sentiment)
    
    return decision