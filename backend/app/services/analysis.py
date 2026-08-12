from dataclasses import dataclass
from urllib.parse import urlparse

from app.schemas.analyze import AnalyzeResponse


@dataclass(slots=True)
class AnalysisService:
    """Orchestrates the analysis flow. Currently returns a controlled placeholder.

    URL validation is conservative here; the request model also validates URLs.
    """

    def _is_valid_url(self, url: str) -> bool:
        p = urlparse(url)
        return p.scheme in ("http", "https") and bool(p.netloc)

    def analyze(self, url: str) -> AnalyzeResponse:
        if not self._is_valid_url(url):
            raise ValueError("invalid url")

        # Placeholder controlled result until analysis modules are implemented
        return AnalyzeResponse(
            url=url,
            seo_score=0,
            aeo_score=0,
            issues=[],
            recommendations=[],
        )
