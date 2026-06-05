
import json
import re
from typing import Any
from agents.base_agent import BaseAgent
from models.schemas import ExtractedEntities, EmailProcessingState
from prompts.agent_prompts import ENTITY_EXTRACTION_PROMPT
from langchain_ollama import OllamaLLM
from config.config import settings


class EntityExtractionAgent(BaseAgent):
    def __init__(self):
        super().__init__("entity_extraction")
        self.llm = OllamaLLM(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url
        )

    def execute(self, state: EmailProcessingState) -> EmailProcessingState:
        self.logger.info(f"Processing email for entity extraction")
        
        try:
            prompt = ENTITY_EXTRACTION_PROMPT.format(email_content=state.email_content)
            response = self.llm.invoke(prompt)
            
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                data = json.loads(json_str)
                
                entities = ExtractedEntities(
                    account_numbers=data.get("account_numbers", []),
                    card_numbers=data.get("card_numbers", []),
                    date_ranges=data.get("date_ranges", []),
                    transaction_counts=data.get("transaction_counts", []),
                    customer_name=data.get("customer_name")
                )
                
                state.entities = entities
                self.logger.info(f"Extracted entities: {entities}")
            else:
                state.entities = ExtractedEntities()
                
        except Exception as e:
            self.logger.error(f"Error in entity extraction: {str(e)}")
            state.entities = ExtractedEntities()
            
        return state
