from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel
from workflows import EmailProcessingWorkflow
from utils import setup_logger
import uvicorn

app = FastAPI(
    title="Intelligent Email Processing System"
)

logger = setup_logger("api")

# Initialize workflow once
workflow = EmailProcessingWorkflow()


class EmailRequest(BaseModel):
    email_content: str


class EmailResponse(BaseModel):
    final_response: str
    sentiment: str
    intents: list[str]


@app.post("/process-email", response_model=EmailResponse)
async def process_email(request: EmailRequest):
    """
    Returns complete response as JSON.
    """
    try:
        logger.info("Received email processing request")

        result = workflow.process_email(request.email_content)

        final_response = result.final_response or "No response generated"

        logger.info(
            f"Generated response:\n{final_response}"
        )

        return EmailResponse(
            final_response=final_response,
            sentiment=result.sentiment.type if result.sentiment else "UNKNOWN",
            intents=[
                intent.type
                for intent in (result.intents or [])
            ]
        )

    except Exception as e:
        logger.error(
            f"Error processing email: {str(e)}",
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@app.post(
    "/process-email/plain",
    response_class=PlainTextResponse
)
async def process_email_plain(request: EmailRequest):
    """
    Returns only the final response as plain text without JSON.
    """
    try:
        logger.info(
            "Received email processing request (plain text)"
        )

        result = workflow.process_email(
            request.email_content
        )

        return result.final_response or "No response generated"

    except Exception as e:
        logger.error(
            f"Error processing email: {str(e)}",
            exc_info=True
        )
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )