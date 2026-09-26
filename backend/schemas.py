"""Pydantic request/response models."""

from typing import Literal, Optional
from pydantic import BaseModel, Field


DocumentType = Literal[
    "Employment Contract",
    "Non-Disclosure Agreement (NDA)",
    "Residential Lease Agreement",
    "Commercial Lease Agreement",
    "Freelance Services Agreement",
    "Consulting Agreement",
    "Partnership Agreement",
    "Sales Agreement",
    "Privacy Policy",
    "Terms of Service",
]


class DocumentRequest(BaseModel):
    document_type: DocumentType = Field(..., description="Type of legal document to generate")
    party_a: str = Field(..., min_length=1, description="First party name / entity")
    party_b: str = Field(..., min_length=1, description="Second party name / entity")
    effective_date: str = Field(..., description="Effective date (YYYY-MM-DD or descriptive)")
    jurisdiction: str = Field(..., description="Governing jurisdiction (e.g. 'State of California, USA')")
    key_terms: str = Field(..., min_length=3, description="Key terms, conditions, and clauses")
    additional_notes: Optional[str] = Field("", description="Optional additional instructions")


class DocumentResponse(BaseModel):
    document_type: str
    content: str
    model: str


class ExportRequest(BaseModel):
    content: str
    filename: str = "document"
    format: Literal["txt", "docx", "pdf"] = "txt"