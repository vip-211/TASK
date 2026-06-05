
from typing import Any
from agents.base_agent import BaseAgent
from models.schemas import EmailProcessingState
from apis.mock_core_apis import MockCoreBankingAPIs
from models.schemas import (
    GetAccountBalanceRequest,
    GetCardTransactionsRequest,
    GetStatementRequest
)
from datetime import datetime


class APIExecutionAgent(BaseAgent):
    def __init__(self, core_apis: MockCoreBankingAPIs):
        super().__init__("api_execution")
        self.core_apis = core_apis

    def execute(self, state: EmailProcessingState) -> EmailProcessingState:
        self.logger.info("Starting API execution")
        
        for request in state.processed_requests:
            if not request.validation_result:
                continue
                
            if request.validation_result["status"] != "VALID":
                continue
                
            intent_type = request.intent.type
            
            if intent_type == "BALANCE_ENQUIRY":
                account = request.validation_result["number"]
                balance_response = self.core_apis.get_account_balance(
                    GetAccountBalanceRequest(account_number=account)
                )
                request.api_response = balance_response.model_dump()
                self.logger.info(f"Fetched balance for {account}")
                
            elif intent_type == "CREDIT_CARD_USAGE":
                card = request.validation_result["number"]
                txn_count = request.entities.transaction_counts[0] if request.entities.transaction_counts else 5
                txn_response = self.core_apis.get_card_transactions(
                    GetCardTransactionsRequest(
                        card_number=card,
                        transaction_count=txn_count
                    )
                )
                request.api_response = txn_response.model_dump()
                self.logger.info(f"Fetched {len(txn_response.transactions)} transactions for {card}")
                
            elif intent_type == "STATEMENT_REQUEST":
                account = request.validation_result["number"]
                month = 4
                year = 2026
                
                if state.entities.date_ranges:
                    date_str = state.entities.date_ranges[0]
                    try:
                        dt = datetime.strptime(date_str, "%B %Y")
                        month = dt.month
                        year = dt.year
                    except:
                        pass
                        
                stmt_response = self.core_apis.get_statement(
                    GetStatementRequest(
                        account_number=account,
                        month=month,
                        year=year
                    )
                )
                request.api_response = stmt_response.model_dump()
                self.logger.info(f"Fetched statement for {account} {month}/{year}")
                
        return state
