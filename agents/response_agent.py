
import json
from typing import Any
from agents.base_agent import BaseAgent
from models.schemas import EmailProcessingState
from prompts.agent_prompts import RESPONSE_GENERATION_PROMPT
from langchain_ollama import OllamaLLM
from config.config import settings


class ResponseGenerationAgent(BaseAgent):
    def __init__(self):
        super().__init__("response_generation")
        self.llm = OllamaLLM(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url
        )

    def _mask_sensitive_data(self, data):
        if isinstance(data, dict):
            masked = {}
            for k, v in data.items():
                if "account" in k.lower() and "number" in k.lower():
                    if len(str(v)) >= 4:
                        masked[k] = "X" * (len(str(v)) - 4) + str(v)[-4:]
                    else:
                        masked[k] = v
                elif "card" in k.lower() and "number" in k.lower():
                    if len(str(v)) >= 4:
                        masked[k] = "XXXX" * ((len(str(v)) // 4) - 1) + str(v)[-4:]
                    else:
                        masked[k] = v
                else:
                    masked[k] = self._mask_sensitive_data(v)
            return masked
        elif isinstance(data, list):
            return [self._mask_sensitive_data(item) for item in data]
        else:
            return data

    def execute(self, state: EmailProcessingState) -> EmailProcessingState:
        self.logger.info("Generating response email")
        
        try:
            processed_data = []
            for req in state.processed_requests:
                req_dict = {
                    "intent": req.intent.type,
                    "validation": req.validation_result,
                    "api_response": self._mask_sensitive_data(req.api_response) if req.api_response else None
                }
                processed_data.append(req_dict)
                
            prompt = RESPONSE_GENERATION_PROMPT.format(
                processed_requests=json.dumps(processed_data, indent=2)
            )
            
            response = self.llm.invoke(prompt)
            state.final_response = response.strip()
            
            self.logger.info("Response generated successfully")
            
        except Exception as e:
            self.logger.error(f"Error in response generation: {str(e)}")
            state.final_response = "Dear Customer,\n\nWe are currently unable to process your request. Please try again later.\n\nThank you,\nCustomer Support Team"
            
        return state
