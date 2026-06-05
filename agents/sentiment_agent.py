
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

    def execute(self, state: EmailProcessingState) -> EmailProcessingState:
        self.logger.info(f"Processing email for sentiment analysis")
        
        try:
            prompt = SENTIMENT_ANALYSIS_PROMPT.format(email_content=state.email_content)
            response = self.llm.invoke(prompt)
            
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                data = json.loads(json_str)
                
                sentiment = Sentiment(
                    type=data.get("type", "NEUTRAL"),
                    confidence=data.get("confidence", 0.9)
                )
                
                state.sentiment = sentiment
                self.logger.info(f"Detected sentiment: {sentiment.type}")
            else:
                state.sentiment = Sentiment(type="NEUTRAL", confidence=0.5)
                
        except Exception as e:
            self.logger.error(f"Error in sentiment analysis: {str(e)}")
            state.sentiment = Sentiment(type="NEUTRAL", confidence=0.5)
            
        return state
