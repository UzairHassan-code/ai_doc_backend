# File path: doc_intel_backend/app/api/schemas.py

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

# --- Response Schemas ---

class UploadResponse(BaseModel):
    """Schema for a successful file upload response."""
    filename: str
    file_id: str
    content_type: str
    saved_path: str
    message: str = "File uploaded successfully."
    timestamp: datetime = Field(default_factory=datetime.now)

class HealthCheck(BaseModel):
    """Schema for API health check."""
    status: str = "ok"
    version: str

# --- Future Schemas (Placeholders for Phase 5) ---

class QueryRequest(BaseModel):
    question: str
    
class QueryResponse(BaseModel):
    answer: str
    sources: List[str]