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