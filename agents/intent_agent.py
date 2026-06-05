
import json
import re
from typing import Any, Dict
from agents.base_agent import BaseAgent
from models.schemas import Intent, EmailProcessingState
from prompts.agent_prompts import INTENT_DETECTION_PROMPT
from langchain_ollama import OllamaLLM
from config.config import settings


class IntentDetectionAgent(BaseAgent):
    def __init__(self):
        super().__init__("intent_detection")
        self.llm = OllamaLLM(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url
        )

    def execute(self, state: EmailProcessingState) -> EmailProcessingState:
        self.logger.info(f"Processing email for intent detection")
        
        try:
            prompt = INTENT_DETECTION_PROMPT.format(email_content=state.email_content)
            response = self.llm.invoke(prompt)
            
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                data = json.loads(json_str)
                
                intents = [
                    Intent(
                        type=intent["type"],
                        confidence=intent.get("confidence", 0.9)
                    )
                    for intent in data.get("intents", [])
                ]
                
                state.intents = intents
                self.logger.info(f"Detected intents: {[i.type for i in intents]}")
            else:
                self.logger.warning("Could not parse intent response")
                
        except Exception as e:
            self.logger.error(f"Error in intent detection: {str(e)}")
            
        return state
