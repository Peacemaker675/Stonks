import numpy as np
from app.schemas.payloads import RegimeSignal
from datetime import datetime

class RegimeDetector:
    def detect_regime(self, market_volatility: float, sentiment_score: float) -> RegimeSignal:
        """
        Logic: Combines VIX-like volatility metrics with aggregated news sentiment.
        """
        regime = "RANGE_BOUND"
        strategy = "MARKET_MAKING"
        
        # Simple Decision Tree Logic (Replace with Random Forest in future)
        if market_volatility > 2.5:
            regime = "HIGH_VOLATILITY"
            strategy = "HALT_TRADING"
            if sentiment_score < -0.5:
                regime = "CRASH_MODE"
                strategy = "AGGRESSIVE_SHORT"
                
        elif sentiment_score > 0.6:
            regime = "BULL_TREND"
            strategy = "MOMENTUM_LONG"
            
        elif sentiment_score < -0.6:
            regime = "BEAR_TREND"
            strategy = "MOMENTUM_SHORT"

        return RegimeSignal(
            current_regime=regime,
            confidence=0.85,  # Mock confidence
            recommended_strategy=strategy,
            action_timestamp=datetime.now()
        )