from fastapi import APIRouter, Depends, HTTPException
from app.services.news_fetcher import NewsAggregator
from app.ml_engine.sentiment_analyzer import SentimentEngine
from app.ml_engine.regime_detector import RegimeDetector
from app.schemas.payloads import RegimeSignal

router = APIRouter()
sentiment_engine = SentimentEngine()
regime_detector = RegimeDetector()
news_aggregator = NewsAggregator() # Assumes you saved the scraper code from previous turn

@router.post("/refresh-intelligence", response_model=RegimeSignal)
async def refresh_market_intelligence():
    """
    Main heartbeat: Scrapes news -> Analyzes Sentiment -> Determines Regime
    """
    # 1. Fetch News
    articles = news_aggregator.get_macro_data()
    if not articles:
        raise HTTPException(status_code=503, detail="News source unavailable")
    
    # 2. Calculate Aggregate Sentiment
    total_score = 0
    for article in articles:
        # Use full text if available, else title
        text = article.get('full_text') or article.get('title')
        total_score += sentiment_engine.analyze(text)
    
    avg_sentiment = total_score / len(articles) if articles else 0
    
    # 3. Detect Regime (Mocking volatility as 1.5 for now)
    decision = regime_detector.detect_regime(market_volatility=1.5, sentiment_score=avg_sentiment)
    
    return decision