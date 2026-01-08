"""
Models Definition.
Pydantic models ensure data validation and generate the OpenAPI schema 
required for Power Platform Custom Connectors.
"""
from pydantic import BaseModel, Field
from typing import List, Optional

class QueryRequest(BaseModel):
    """
    The input payload for the Chat endpoint.
    """
    question: str = Field(..., description="The user's question about Energy Regulations.")
    context_filter: Optional[str] = Field("general", description="Scope: 'general', 'audit', or 'compliance'.")

class SourceCitation(BaseModel):
    """
    Represents a reference to a document.
    """
    document: str
    section: str

class QueryResponse(BaseModel):
    """
    The output payload containing the AI's answer.
    """
    answer: str = Field(..., description="The AI generated response.")
    citations: List[SourceCitation] = Field(default=[], description="References to the source material.")
    confidence_score: float = Field(0.95, description="Simulated confidence metric.")