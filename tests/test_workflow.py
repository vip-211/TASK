
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from workflows import EmailProcessingWorkflow


def test_sample_emails():
    workflow = EmailProcessingWorkflow()
    
    sample_emails = [
        "Please provide my savings account balance for account number 1234567890.",
        "Please share my last 5 credit card transactions for card 456712348901.",
        "Kindly send my bank statement for April 2026.",
        "Please share my account balance for account 1234567890 and also send last 3 transactions of my credit card 9876543210.",
        "Please provide balance for account 1234567890 and card transactions for card 999999999."
    ]
    
    for i, email in enumerate(sample_emails, 1):
        print(f"\n{'='*60}")
        print(f"Test Scenario {i}")
        print(f"{'='*60}")
        print(f"Email: {email}\n")
        
        result = workflow.process_email(email)
        
        print(f"Sentiment: {result.sentiment.type if result.sentiment else 'N/A'}")
        print(f"Intents: {[intent.type for intent in result.intents]}")
        print(f"\nResponse:\n{result.final_response}")


if __name__ == "__main__":
    test_sample_emails()
