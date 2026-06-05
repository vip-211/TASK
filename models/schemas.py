
from pydantic import BaseModel, Field
from typing import List, Optional, Literal


class ValidateAccountRequest(BaseModel):
    account_number: str = Field(..., description="Account number to validate")


class ValidateAccountResponse(BaseModel):
    status: Literal["VALID", "INVALID"]
    customer_name: Optional[str] = None


class ValidateCardRequest(BaseModel):
    card_number: str = Field(..., description="Credit card number to validate")


class ValidateCardResponse(BaseModel):
    status: Literal["VALID", "INVALID"]
    customer_name: Optional[str] = None


class GetAccountBalanceRequest(BaseModel):
    account_number: str


class GetAccountBalanceResponse(BaseModel):
    account_number: str
    available_balance: float
    currency: str = "INR"


class GetCardTransactionsRequest(BaseModel):
    card_number: str
    transaction_count: Optional[int] = 5


class Transaction(BaseModel):
    date: str
    description: str
    amount: float
    type: Literal["DEBIT", "CREDIT"]


class GetCardTransactionsResponse(BaseModel):
    card_number: str
    transactions: List[Transaction]


class GetStatementRequest(BaseModel):
    account_number: str
    month: int
    year: int


class StatementEntry(BaseModel):
    date: str
    description: str
    debit: Optional[float] = None
    credit: Optional[float] = None
    balance: float


class GetStatementResponse(BaseModel):
    account_number: str
    month: int
    year: int
    entries: List[StatementEntry]


class Intent(BaseModel):
    type: Literal["BALANCE_ENQUIRY", "CREDIT_CARD_USAGE", "STATEMENT_REQUEST"]
    confidence: float


class Sentiment(BaseModel):
    type: Literal["NEUTRAL", "POSITIVE", "NEGATIVE", "URGENT"]
    confidence: float


class ExtractedEntities(BaseModel):
    account_numbers: List[str] = Field(default_factory=list)
    card_numbers: List[str] = Field(default_factory=list)
    date_ranges: List[str] = Field(default_factory=list)
    transaction_counts: List[int] = Field(default_factory=list)
    customer_name: Optional[str] = None


class ProcessedRequest(BaseModel):
    intent: Intent
    entities: ExtractedEntities
    validation_result: Optional[dict] = None
    api_response: Optional[dict] = None


class EmailProcessingState(BaseModel):
    email_content: str
    intents: List[Intent] = Field(default_factory=list)
    sentiment: Optional[Sentiment] = None
    entities: Optional[ExtractedEntities] = None
    processed_requests: List[ProcessedRequest] = Field(default_factory=list)
    final_response: Optional[str] = None
