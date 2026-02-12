from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime

class NewsItem(BaseModel):
    title: str
    source: str
    published_at: str
    sentiment_score: float = 0.0

class RegimeSignal(BaseModel):
    current_regime: str  # e.g., "BULL_TREND", "HIGH_VOLATILITY"
    confidence: float
    recommended_strategy: str
    action_timestamp: datetime
    
class HealthCheck(BaseModel):
    status: str
    version: str

class MarketTick(BaseModel):
    timestamp: datetime
    price: float
    open: float
    high: float
    low: float
    close: float
    volume: int 
    volatility_1h: float
    vix_proxy: float
    sma_50: float
    dist_sma_50: float
    sma_200: float
    dist_sma_200: float
    regime_vol: float
    return_1h: float = Field(alias="1h_return") 
    sentiment_score: float

