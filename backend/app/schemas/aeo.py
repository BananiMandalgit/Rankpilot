# backend/app/schemas/aeo.py

from pydantic import BaseModel, Field
from typing import List, Optional


class AEOResult(BaseModel):
    """
    Output of the AEO (Answer Engine Optimization) analyzer.
    Consumed by Member 6's /api/analyze endpoint.
    """
    aeo_score: int = Field(default=0, ge=0, le=100)
    issues: List[str] = Field(default_factory=list)

    # --- enhancement fields (additive, all optional) ---
    # None = check was not evaluated (e.g. raw_html not available yet)
    structured_data_ok: Optional[bool] = None
    schema_types_found: List[str] = Field(default_factory=list)
    qa_structure_ok: Optional[bool] = None
    freshness_signals_ok: Optional[bool] = None