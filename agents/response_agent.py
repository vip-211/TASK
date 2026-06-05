
from typing import Any
from agents.base_agent import BaseAgent
from models.schemas import EmailProcessingState


class ResponseGenerationAgent(BaseAgent):
    def __init__(self):
        super().__init__("response_generation")

    def execute(self, state: EmailProcessingState) -> EmailProcessingState:
        self.logger.info("Generating response email")
        
        try:
            # Process each request and build response parts
            response_parts = []
            for req in state.processed_requests:
                intent = req.intent.type
                
                if intent == "BALANCE_ENQUIRY":
                    if req.validation_result:
                        if req.validation_result["status"] == "VALID":
                            if req.api_response:
                                balance = req.api_response.get("available_balance", 0)
                                acc_num = req.api_response.get("account_number", "XXXX")
                                masked_acc = "X"*(len(acc_num)-4) + acc_num[-4:]
                                response_parts.append(f"Your account balance for account {masked_acc} is Rs.{balance:.2f}.")
                        else:
                            response_parts.append("Invalid account details provided.")
                    else:
                        response_parts.append("Please provide your account number.")
                
                elif intent == "CREDIT_CARD_USAGE":
                    if req.validation_result:
                        if req.validation_result["status"] == "VALID":
                            if req.api_response:
                                card = req.validation_result.get("number", "XXXX")
                                stripped = card.replace(" ", "").replace("-", "").replace("X", "").replace("x", "")
                                masked_card = "XXXX-XXXX-XXXX-" + stripped[-4:]
                                transactions = req.api_response.get("transactions", [])
                                txn_list = "\n".join([
                                    f"- {txn['date']}: {txn['description']} - Rs.{txn['amount']:.2f} ({txn['type']})" 
                                    for txn in transactions
                                ])
                                response_parts.append(f"Your last {len(transactions)} credit card transactions for card {masked_card} are:\n{txn_list}")
                        else:
                            response_parts.append("Invalid credit card details provided.")
                    else:
                        response_parts.append("Please provide your credit card number.")
                
                elif intent == "STATEMENT_REQUEST":
                    if req.validation_result:
                        if req.validation_result["status"] == "VALID":
                            response_parts.append("Your request is successful. Here is your statement. Click here to download.")
                        else:
                            response_parts.append("Invalid account details provided.")
                    else:
                        response_parts.append("Your request is successful. Here is your statement. Click here to download.")
            
            # Build final response
            if response_parts:
                full_response = "Dear Customer,\n\n" + "\n\n".join(response_parts) + "\n\nThank you,\nCustomer Support Team"
                state.final_response = full_response
            else:
                state.final_response = "Dear Customer,\n\nWe are currently unable to process your request. Please try again later.\n\nThank you,\nCustomer Support Team"
            
            self.logger.info("Response generated successfully")
            
        except Exception as e:
            self.logger.error(f"Error in response generation: {str(e)}")
            state.final_response = "Dear Customer,\n\nWe are currently unable to process your request. Please try again later.\n\nThank you,\nCustomer Support Team"
            
        return state
