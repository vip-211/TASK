
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from workflows import EmailProcessingWorkflow
from utils import setup_logger
import uvicorn

app = FastAPI(title="Intelligent Email Processing System")
logger = setup_logger("api")

workflow = EmailProcessingWorkflow()


class EmailRequest(BaseModel):
    email_content: str


class EmailResponse(BaseModel):
    final_response: str
    sentiment: str
    intents: list


@app.post("/process-email", response_model=EmailResponse)
async def process_email(request: EmailRequest):
    try:
        logger.info("Received email processing request")
        result = workflow.process_email(request.email_content)
        
        return EmailResponse(
            final_response=result.final_response or "No response generated",
            sentiment=result.sentiment.type if result.sentiment else "UNKNOWN",
            intents=[intent.type for intent in result.intents]
        )
    except Exception as e:
        logger.error(f"Error processing email: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
