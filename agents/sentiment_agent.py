
import json
import re
from typing import Any
from agents.base_agent import BaseAgent
from models.schemas import Sentiment, EmailProcessingState
from prompts.agent_prompts import SENTIMENT_ANALYSIS_PROMPT
from langchain_ollama import OllamaLLM
from config.config import settings


class SentimentAnalysisAgent(BaseAgent):
    def __init__(self):
        super().__init__("sentiment_analysis")
        self.llm = OllamaLLM(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url
        )
        
    def _rule_based_sentiment(self, email_content: str):
        content_lower = email_content.lower()
        # Check for urgent keywords first
        urgent_keywords = ["urgent", "asap", "immediately", "emergency", "critical"]
        if any(keyword in content_lower for keyword in urgent_keywords):
            return Sentiment(type="URGENT", confidence=0.95)
        # Check for positive keywords
        positive_keywords = ["thank", "thanks", "great", "happy", "satisfied", "excellent"]
        if any(keyword in content_lower for keyword in positive_keywords):
            return Sentiment(type="POSITIVE", confidence=0.95)
        # Check for negative keywords
        negative_keywords = ["angry", "frustrated", "annoyed", "terrible", "bad", "worst"]
        if any(keyword in content_lower for keyword in negative_keywords):
            return Sentiment(type="NEGATIVE", confidence=0.95)
        # Default to neutral
        return Sentiment(type="NEUTRAL", confidence=0.95)

    def execute(self, state: EmailProcessingState) -> EmailProcessingState:
        self.logger.info(f"Processing email for sentiment analysis")
        
        try:
            # Try rule-based first
            sentiment = self._rule_based_sentiment(state.email_content)
            state.sentiment = sentiment
            self.logger.info(f"Detected sentiment (rule-based): {sentiment.type}")
            return state
                
        except Exception as e:
            self.logger.error(f"Error in sentiment analysis: {str(e)}")
            state.sentiment = Sentiment(type="NEUTRAL", confidence=0.5)
            
        return state
