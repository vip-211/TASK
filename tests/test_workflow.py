
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from workflows import EmailProcessingWorkflow
from models.schemas import EmailProcessingState

# Sample test cases (each is a tuple: (email_content, expected_intents))
SAMPLE_TEST_CASES = [
    ("Please provide my savings account balance for account number 1234567890.", ["BALANCE_ENQUIRY"]),
    ("Please share my last 5 credit card transactions for card 4567XXXX8901.", ["CREDIT_CARD_USAGE"]),
    ("Kindly send my bank statement for April 2026.", ["STATEMENT_REQUEST"]),
    ("Please share my account balance for account 1234567890 and also send last 3 transactions of my credit card 9876543210.", ["BALANCE_ENQUIRY", "CREDIT_CARD_USAGE"]),
    ("Please provide balance for account 1234567890 and card transactions for card 999999999.", ["BALANCE_ENQUIRY", "CREDIT_CARD_USAGE"]),
]

@pytest.fixture
def workflow():
    """Fixture to create and return an EmailProcessingWorkflow instance."""
    return EmailProcessingWorkflow()

@pytest.mark.parametrize("email_content, expected_intents", SAMPLE_TEST_CASES)
def test_email_workflow(workflow, email_content, expected_intents):
    """Test end-to-end email processing workflow for various scenarios."""
    # Process the email
    result = workflow.process_email(email_content)
    
    # Verify the result is an EmailProcessingState instance
    assert isinstance(result, EmailProcessingState)
    # Verify we have intents
    assert len(result.intents) > 0
    # Verify sentiment is present
    assert result.sentiment is not None
    # Verify final response is generated
    assert result.final_response is not None
    assert len(result.final_response.strip()) > 0
    
    # Optional: Print details (visible when using pytest -s)
    print(f"\nTest Email: {email_content}")
    print(f"Detected Intents: {[intent.type for intent in result.intents]}")
    print(f"Detected Sentiment: {result.sentiment.type}")
    print(f"Final Response:\n{result.final_response}\n")
