
from typing import TypedDict, Annotated, Sequence
from langgraph.graph import StateGraph, END
from models.schemas import EmailProcessingState
from agents import (
    IntentDetectionAgent,
    SentimentAnalysisAgent,
    EntityExtractionAgent,
    ValidationAgent,
    APIExecutionAgent,
    ResponseGenerationAgent
)
from apis import MockCoreBankingAPIs
from utils import setup_logger


class EmailProcessingWorkflow:
    def __init__(self):
        self.logger = setup_logger("workflow")
        self.core_apis = MockCoreBankingAPIs()
        
        self.intent_agent = IntentDetectionAgent()
        self.sentiment_agent = SentimentAnalysisAgent()
        self.entity_agent = EntityExtractionAgent()
        self.validation_agent = ValidationAgent(self.core_apis)
        self.api_agent = APIExecutionAgent(self.core_apis)
        self.response_agent = ResponseGenerationAgent()
        
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        graph = StateGraph(EmailProcessingState)
        
        graph.add_node("intent_detection", self._intent_detection_node)
        graph.add_node("sentiment_analysis", self._sentiment_analysis_node)
        graph.add_node("entity_extraction", self._entity_extraction_node)
        graph.add_node("validation", self._validation_node)
        graph.add_node("api_execution", self._api_execution_node)
        graph.add_node("response_generation", self._response_generation_node)
        
        graph.set_entry_point("intent_detection")
        graph.add_edge("intent_detection", "sentiment_analysis")
        graph.add_edge("sentiment_analysis", "entity_extraction")
        graph.add_edge("entity_extraction", "validation")
        graph.add_edge("validation", "api_execution")
        graph.add_edge("api_execution", "response_generation")
        graph.add_edge("response_generation", END)
        
        return graph.compile()

    def _intent_detection_node(self, state: EmailProcessingState) -> EmailProcessingState:
        return self.intent_agent.execute(state)

    def _sentiment_analysis_node(self, state: EmailProcessingState) -> EmailProcessingState:
        return self.sentiment_agent.execute(state)

    def _entity_extraction_node(self, state: EmailProcessingState) -> EmailProcessingState:
        return self.entity_agent.execute(state)

    def _validation_node(self, state: EmailProcessingState) -> EmailProcessingState:
        return self.validation_agent.execute(state)

    def _api_execution_node(self, state: EmailProcessingState) -> EmailProcessingState:
        return self.api_agent.execute(state)

    def _response_generation_node(self, state: EmailProcessingState) -> EmailProcessingState:
        return self.response_agent.execute(state)

    def process_email(self, email_content: str) -> EmailProcessingState:
        self.logger.info("Starting email processing workflow")
        
        initial_state = EmailProcessingState(email_content=email_content)
        final_state_dict = self.graph.invoke(initial_state)
        final_state = EmailProcessingState(**final_state_dict)
        
        self.logger.info("Email processing workflow completed")
        return final_state
