import pandas as pd

class MarketFeeder:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.index = 0
        
    def get_next_tick(self):
        """Returns the next row as a dictionary, or None if finished."""
        if self.index >= len(self.df):
            return None
            
        row = self.df.iloc[self.index]
        self.index += 1
        return {
            "timestamp": row['date'],
            "price": row['close'],
            "open": row['open'],
            "high": row['high'],
            "low": row['low'],
            "close": row['close'],
            "volume": row['volume'],
            "volatility_1h": row['volatility_1h'],
            "vix_proxy": row['vix_proxy'],
            "sma_50": row['sma_50'],
            "dist_sma_50": row['dist_sma_50'],
            "sma_200": row['sma_200'],
            "dist_sma_200": row['dist_sma_200'],
            "regime_vol": row['regime_vol'],
            "1h_return": row['1h_return'],
            "sentiment_score": row['sentiment_score']
        }
