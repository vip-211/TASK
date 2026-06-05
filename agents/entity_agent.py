

import re
from typing import Any
from agents.base_agent import BaseAgent
from models.schemas import ExtractedEntities, EmailProcessingState


class EntityExtractionAgent(BaseAgent):
    def __init__(self):
        super().__init__("entity_extraction")

    def _rule_based_entity_extraction(self, email_content: str):
        account_numbers = []
        card_numbers = []
        date_ranges = []
        transaction_counts = []
        
        # Extract account numbers (digits, possibly with X's)
        account_pattern = r'\b(?:account\s+number[:\s]*|a/c[:\s]*|acct[:\s]*)?([\dX]{6,})\b'
        for match in re.finditer(account_pattern, email_content, re.IGNORECASE):
            if len(match.group(1)) >= 6:
                account_numbers.append(match.group(1))
                
        # Extract card numbers (digits, possibly with X's, spaces, hyphens)
        card_pattern = r'\b(?:card[:\s]*|credit\s+card[:\s]*|debit\s+card[:\s]*)?([\dX\s-]{8,})\b'
        for match in re.finditer(card_pattern, email_content, re.IGNORECASE):
            card_candidate = match.group(1).strip()
            # Clean up
            cleaned = re.sub(r'[\s-]', '', card_candidate)
            if len(cleaned) >= 8:
                card_numbers.append(card_candidate)
                
        # Extract date ranges (month year)
        month_year_pattern = r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{4})\b'
        for match in re.finditer(month_year_pattern, email_content, re.IGNORECASE):
            date_ranges.append(f"{match.group(1)} {match.group(2)}")
            
        # Extract transaction counts
        txn_count_pattern = r'\b(?:last|latest)\s+(\d+)\s*(?:credit\s+card)?\s*(?:transaction|txn)'
        for match in re.finditer(txn_count_pattern, email_content, re.IGNORECASE):
            try:
                count = int(match.group(1))
                if count > 0:
                    transaction_counts.append(count)
            except:
                pass
        # Fallback if above not found
        fallback_count_pattern = r'\b(\d+)\s+(?:credit\s+card)?\s*(?:transaction|txn)'
        for match in re.finditer(fallback_count_pattern, email_content, re.IGNORECASE):
            try:
                count = int(match.group(1))
                if count > 0 and count not in transaction_counts:
                    transaction_counts.append(count)
            except:
                pass
                
        return ExtractedEntities(
            account_numbers=account_numbers,
            card_numbers=card_numbers,
            date_ranges=date_ranges,
            transaction_counts=transaction_counts
        )

    def execute(self, state: EmailProcessingState) -> EmailProcessingState:
        self.logger.info("Processing email for entity extraction")
        
        try:
            # Use only rule-based
            entities = self._rule_based_entity_extraction(state.email_content)
            state.entities = entities
            self.logger.info(f"Extracted entities: {entities}")
                
        except Exception as e:
            self.logger.error(f"Error in entity extraction: {str(e)}", exc_info=True)
            state.entities = ExtractedEntities()
            
        return state
