import torch
from transformers import pipeline
import logging

logger = logging.getLogger(__name__)

class SentimentEngine:
    _instance = None
    _pipeline = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SentimentEngine, cls).__new__(cls)
            cls._instance._load_model()
        return cls._instance

    def _load_model(self):
        try:
            logger.info("Loading FinBERT model...")
            # We use a smaller, distilled model for speed in this simulation
            # In real prod, use "ProsusAI/finbert"
            self._pipeline = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                device=0 if torch.cuda.is_available() else -1
            )
            logger.info("Model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load ML model: {e}")
            self._pipeline = None

    def analyze(self, text: str) -> float:
        """
        Returns a score between -1.0 (Negative) and 1.0 (Positive)
        """
        if not self._pipeline:
            return 0.0
        
        # Truncate text to 512 tokens to prevent model crash
        result = self._pipeline(text[:512])[0]
        score = result['score']
        label = result['label']
        
        if label == 'NEGATIVE':
            return -score
        return score