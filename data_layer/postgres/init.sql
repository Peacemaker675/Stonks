CREATE TABLE IF NOT EXISTS market_regimes (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    regime_name VARCHAR(50) NOT NULL,
    confidence FLOAT,
    trigger_source VARCHAR(50) -- e.g., "News", "Technical"
);

CREATE TABLE IF NOT EXISTS trade_logs (
    trade_id VARCHAR(50) PRIMARY KEY,
    symbol VARCHAR(20),
    price DECIMAL(10, 2),
    quantity INT,
    side VARCHAR(4), -- BUY/SELL
    strategy_used VARCHAR(50),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS news_sentiment (
    id SERIAL PRIMARY KEY,
    headline TEXT,
    source VARCHAR(50),
    sentiment_score FLOAT,
    raw_url TEXT,
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);