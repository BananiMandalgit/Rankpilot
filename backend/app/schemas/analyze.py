from pydantic import BaseModel, HttpUrl, Field
from typing import List


class AnalyzeRequest(BaseModel):
    url: HttpUrl


class AnalyzeResponse(BaseModel):
    url: HttpUrl
    seo_score: int = 0
    aeo_score: int = 0
    issues: List[str] = Field(default_factory=list)
    recommendations: List[str] = Field(default_factory=list)
