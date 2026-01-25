from fastapi.testclient import TestClient
from app.main import app
from app.services.news_fetcher import NewsAggregator
from unittest.mock import MagicMock

client = TestClient(app)

# --- Mocking External Dependencies ---
# We don't want to actually scrape the web during tests!
def mock_get_macro_data():
    return [
        {"title": "Market is Crashing", "sentiment_score": -0.9},
        {"title": "Oil Prices Surge", "sentiment_score": -0.5}
    ]

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "Intelligence Layer"}

def test_refresh_intelligence_flow(monkeypatch):
    """
    Test the full loop: Scrape -> Sentiment -> Regime
    We use 'monkeypatch' to replace the real NewsAggregator with our mock.
    """
    
    # Mock the method 'get_macro_data' on the NewsAggregator class
    monkeypatch.setattr(
        "app.services.news_fetcher.NewsAggregator.get_macro_data", 
        mock_get_macro_data
    )

    response = client.post("/api/v1/refresh-intelligence")
    
    assert response.status_code == 200
    data = response.json()
    
    # Assert that our negative news mock caused a negative regime
    assert data["recommended_strategy"] in ["AGGRESSIVE_SHORT", "MOMENTUM_SHORT"]
    assert "current_regime" in data