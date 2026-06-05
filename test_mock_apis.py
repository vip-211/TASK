
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from apis import MockCoreBankingAPIs
from models import (
    ValidateAccountRequest,
    ValidateCardRequest,
    GetAccountBalanceRequest,
    GetCardTransactionsRequest,
    GetStatementRequest
)


def test_mock_apis():
    core_apis = MockCoreBankingAPIs()
    
    print("Testing ValidateAccount API...")
    resp = core_apis.validate_account(ValidateAccountRequest(account_number="1234567890"))
    print(f"Result: {resp}")
    
    print("\nTesting ValidateCard API...")
    resp = core_apis.validate_card(ValidateCardRequest(card_number="456712348901"))
    print(f"Result: {resp}")
    
    print("\nTesting GetAccountBalance API...")
    resp = core_apis.get_account_balance(GetAccountBalanceRequest(account_number="1234567890"))
    print(f"Result: {resp}")
    
    print("\nTesting GetCardTransactions API...")
    resp = core_apis.get_card_transactions(GetCardTransactionsRequest(card_number="456712348901", transaction_count=3))
    print(f"Result: {resp}")
    
    print("\nTesting GetStatement API...")
    resp = core_apis.get_statement(GetStatementRequest(account_number="1234567890", month=4, year=2026))
    print(f"Result: {resp}")


if __name__ == "__main__":
    test_mock_apis()
