
from typing import Any
from agents.base_agent import BaseAgent
from models.schemas import EmailProcessingState, ProcessedRequest, Intent
from apis.mock_core_apis import MockCoreBankingAPIs
from models.schemas import ValidateAccountRequest, ValidateCardRequest


class ValidationAgent(BaseAgent):
    def __init__(self, core_apis: MockCoreBankingAPIs):
        super().__init__("validation")
        self.core_apis = core_apis

    def execute(self, state: EmailProcessingState) -> EmailProcessingState:
        self.logger.info("Starting validation of extracted entities")
        
        processed_requests = []
        
        if not state.entities:
            return state
            
        for intent in state.intents:
            request = ProcessedRequest(intent=intent, entities=state.entities)
            
            if intent.type == "BALANCE_ENQUIRY":
                if state.entities.account_numbers:
                    account = state.entities.account_numbers[0]
                    validation = self.core_apis.validate_account(
                        ValidateAccountRequest(account_number=account)
                    )
                    request.validation_result = {
                        "type": "account",
                        "number": account,
                        "status": validation.status,
                        "customer_name": validation.customer_name
                    }
                    
            elif intent.type == "CREDIT_CARD_USAGE":
                if state.entities.card_numbers:
                    card = state.entities.card_numbers[0]
                    validation = self.core_apis.validate_card(
                        ValidateCardRequest(card_number=card)
                    )
                    request.validation_result = {
                        "type": "card",
                        "number": card,
                        "status": validation.status,
                        "customer_name": validation.customer_name
                    }
                    
            elif intent.type == "STATEMENT_REQUEST":
                if state.entities.account_numbers:
                    account = state.entities.account_numbers[0]
                    validation = self.core_apis.validate_account(
                        ValidateAccountRequest(account_number=account)
                    )
                    request.validation_result = {
                        "type": "account",
                        "number": account,
                        "status": validation.status,
                        "customer_name": validation.customer_name
                    }
                    
            processed_requests.append(request)
            
        state.processed_requests = processed_requests
        self.logger.info(f"Validated {len(processed_requests)} requests")
        
        return state
