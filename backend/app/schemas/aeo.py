# backend/app/schemas/aeo.py

from pydantic import BaseModel, Field
from typing import List


class AEOResult(BaseModel):
    """
    Output of the AEO (Answer Engine Optimization) analyzer.
    Consumed by Member 6's /api/analyze endpoint.
    """
    aeo_score: int = Field(default=0, ge=0, le=100)
    issues: List[str] = Field(default_factory=list)