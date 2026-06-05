
from models.schemas import (
    ValidateAccountRequest,
    ValidateAccountResponse,
    ValidateCardRequest,
    ValidateCardResponse,
    GetAccountBalanceRequest,
    GetAccountBalanceResponse,
    GetCardTransactionsRequest,
    GetCardTransactionsResponse,
    GetStatementRequest,
    GetStatementResponse,
    Transaction,
    StatementEntry
)
from typing import Dict


class MockCoreBankingAPIs:
    def __init__(self):
        self.valid_accounts: Dict[str, str] = {
            "1234567890": "John Doe",
            "0987654321": "Jane Smith",
            "1122334455": "Bob Johnson"
        }
        self.valid_cards: Dict[str, str] = {
            "456712348901": "John Doe",
            "9876543210": "Jane Smith",
            "1234987654": "Bob Johnson"
        }
        self.account_balances: Dict[str, float] = {
            "1234567890": 125000.00,
            "0987654321": 250000.50,
            "1122334455": 75000.00
        }
        self.card_transactions = {
            "456712348901": [
                Transaction(date="2026-05-01", description="Groceries", amount=1500.00, type="DEBIT"),
                Transaction(date="2026-05-03", description="Salary", amount=50000.00, type="CREDIT"),
                Transaction(date="2026-05-05", description="Fuel", amount=800.00, type="DEBIT"),
                Transaction(date="2026-05-07", description="Shopping", amount=3500.00, type="DEBIT"),
                Transaction(date="2026-05-10", description="Restaurant", amount=2000.00, type="DEBIT"),
                Transaction(date="2026-05-12", description="Utilities", amount=1200.00, type="DEBIT")
            ],
            "9876543210": [
                Transaction(date="2026-05-02", description="Online Shopping", amount=4500.00, type="DEBIT"),
                Transaction(date="2026-05-04", description="Refund", amount=500.00, type="CREDIT"),
                Transaction(date="2026-05-06", description="Coffee", amount=150.00, type="DEBIT")
            ]
        }
        self.statements = {
            ("1234567890", 4, 2026): [
                StatementEntry(date="2026-04-01", description="Opening Balance", credit=None, debit=None, balance=100000.00),
                StatementEntry(date="2026-04-05", description="Deposit", credit=50000.00, debit=None, balance=150000.00),
                StatementEntry(date="2026-04-10", description="Withdrawal", credit=None, debit=25000.00, balance=125000.00),
                
            ]
        }

    def validate_account(self, request: ValidateAccountRequest) -> ValidateAccountResponse:
        account = request.account_number.replace(" ", "").replace("-", "").replace("X", "").replace("x", "")
        if account in self.valid_accounts:
            return ValidateAccountResponse(
                status="VALID",
                customer_name=self.valid_accounts[account]
            )
        return ValidateAccountResponse(status="INVALID")

    def _find_matching_card(self, stripped_card: str):
        """Find a valid card that matches the stripped number (handles various masked cards)"""
        if stripped_card in self.valid_cards:
            return stripped_card
        
        
        for valid_card in self.valid_cards.keys():
            if valid_card.endswith(stripped_card):
                return valid_card
        
        # If stripped_card has at least 4 digits
        if len(stripped_card) >= 8:
            first_4 = stripped_card[:4]
            last_4 = stripped_card[-4:]
            for valid_card in self.valid_cards.keys():
                if valid_card.startswith(first_4) and valid_card.endswith(last_4):
                    return valid_card
        return None

    def validate_card(self, request: ValidateCardRequest) -> ValidateCardResponse:
        card = request.card_number.replace(" ", "").replace("-", "").replace("X", "").replace("x", "")
        matching_card = self._find_matching_card(card)
        if matching_card:
            return ValidateCardResponse(
                status="VALID",
                customer_name=self.valid_cards[matching_card]
            )
        return ValidateCardResponse(status="INVALID")

    def get_account_balance(self, request: GetAccountBalanceRequest) -> GetAccountBalanceResponse:
        account = request.account_number.replace(" ", "").replace("-", "").replace("X", "").replace("x", "")
        return GetAccountBalanceResponse(
            account_number=request.account_number,
            available_balance=self.account_balances.get(account, 0.00),
            currency="INR"
        )

    def get_card_transactions(self, request: GetCardTransactionsRequest) -> GetCardTransactionsResponse:
        card = request.card_number.replace(" ", "").replace("-", "").replace("X", "").replace("x", "")
        matching_card = self._find_matching_card(card)
        transactions = self.card_transactions.get(matching_card, [])
        count = request.transaction_count or 5
        return GetCardTransactionsResponse(
            card_number=request.card_number,
            transactions=transactions[:count]
        )

    def get_statement(self, request: GetStatementRequest) -> GetStatementResponse:
        key = (request.account_number, request.month, request.year)
        return GetStatementResponse(
            account_number=request.account_number,
            month=request.month,
            year=request.year,
            entries=self.statements.get(key, [])
        )
