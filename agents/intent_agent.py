

from typing import Any, Dict
from agents.base_agent import BaseAgent
from models.schemas import Intent, EmailProcessingState


class IntentDetectionAgent(BaseAgent):
    def __init__(self):
        super().__init__("intent_detection")

    def _rule_based_intent_detection(self, email_content: str):
        intents = []
        content_lower = email_content.lower()
        
        if any(keyword in content_lower for keyword in ["balance", "account balance"]):
            intents.append(Intent(type="BALANCE_ENQUIRY", confidence=0.95))
        if any(keyword in content_lower for keyword in ["credit card", "card transaction", "transactions"]):
            intents.append(Intent(type="CREDIT_CARD_USAGE", confidence=0.95))
        if any(keyword in content_lower for keyword in ["statement", "bank statement"]):
            intents.append(Intent(type="STATEMENT_REQUEST", confidence=0.95))
        
        return intents

    def execute(self, state: EmailProcessingState) -> EmailProcessingState:
        self.logger.info("Processing email for intent detection")
        
        try:
            # Use only rule-based
            intents = self._rule_based_intent_detection(state.email_content)
            state.intents = intents
            self.logger.info(f"Detected intents: {[i.type for i in intents]}")
                
        except Exception as e:
            self.logger.error(f"Error in intent detection: {str(e)}")
            
        return state
