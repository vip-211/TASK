
# Intelligent Email Processing & Automated Customer Response System

An AI-powered banking email automation system using Python, LangChain, LangGraph, and LLaMA.

## Prerequisites

- Python 3.10+
- Ollama installed locally (https://ollama.com)
- LLaMA 3.2 model pulled: `ollama pull llama3.2`

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
   - Windows (PowerShell):
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - Windows (Command Prompt):
     ```cmd
     venv\Scripts\activate.bat
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

1. Start Ollama (if not already running)
2. Make sure your virtual environment is activated (see Installation)
3. Run the FastAPI server:
```bash
python main.py
```
4. Access the API docs at http://localhost:8000/docs

## Testing the Mock APIs

To test the mock core banking APIs without Ollama:
```bash
python test_mock_apis.py
```

## Running the Full Workflow Tests

To test the complete email processing workflow (requires Ollama with llama3.2):
```bash
python tests/test_workflow.py
```

## Project Structure

```
project/
├── agents/          # Agent implementations
├── apis/            # Mock core banking APIs
├── models/          # Pydantic schemas
├── prompts/         # Agent prompts
├── workflows/       # LangGraph workflow orchestration
├── utils/           # Utility functions
├── tests/           # Tests
├── config/          # Configuration
├── logs/            # Log files
├── main.py          # FastAPI entry point
└── requirements.txt
```

## Sample Emails

### Scenario 1: Account Balance Enquiry
```
Please provide my savings account balance for account number 1234567890.
```

### Scenario 2: Credit Card Usage
```
Please share my last 5 credit card transactions for card 456712348901.
```

### Scenario 3: Statement Request
```
Kindly send my bank statement for April 2026.
```

### Scenario 4: Multiple Requests
```
Please share my account balance for account 1234567890 and also send last 3 transactions of my credit card 9876543210.
```

### Scenario 5: Partial Validation Failure
```
Please provide balance for account 1234567890 and card transactions for card 999999999.
```
