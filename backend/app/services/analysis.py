from dataclasses import dataclass
from urllib.parse import urlparse

from app.schemas.analyze import AnalyzeResponse
from crawler.src.services.crawler_service import CrawlerService
from seo.src.seo_analyzer import SEOAnalyzer


@dataclass(slots=True)
class AnalysisService:
    """Orchestrates URL validation, crawling, and deterministic SEO analysis.

    URL validation is conservative here; the request model also validates URLs.
    """

    def _is_valid_url(self, url: str) -> bool:
        p = urlparse(url)
        return p.scheme in ("http", "https") and bool(p.netloc)

    def analyze(self, url: str) -> AnalyzeResponse:
        if not self._is_valid_url(url):
            raise ValueError("invalid url")

        try:
            page_data = CrawlerService().fetch_and_extract(url)
        except Exception as exc:
            return AnalyzeResponse(
                url=url,
                seo_score=0,
                aeo_score=0,
                issues=[f"Crawler error: {str(exc)}"],
                recommendations=[],
            )

        if page_data.error:
            return AnalyzeResponse(
                url=url,
                seo_score=0,
                aeo_score=0,
                issues=[page_data.error],
                recommendations=[],
            )

        seo_result = SEOAnalyzer().analyze(page_data)

        return AnalyzeResponse(
            url=url,
            seo_score=seo_result.score,
            aeo_score=0,
            issues=seo_result.issues,
            recommendations=[],
        )
