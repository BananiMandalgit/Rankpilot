from dataclasses import dataclass
from typing import TYPE_CHECKING
from urllib.parse import urlparse

from app.schemas.analyze import AnalyzeResponse
from crawler.src.parsers.html_parser import PageData
from crawler.src.services.crawler_service import CrawlerService
from seo.src.seo_analyzer import SEOAnalyzer

if TYPE_CHECKING:
    from ai.src.clients.base import AIClientProtocol


@dataclass(slots=True)
class AnalysisService:
    """Orchestrates URL validation, crawling, and deterministic SEO analysis.

    URL validation is conservative here; the request model also validates URLs.
    """

    def _is_valid_url(self, url: str) -> bool:
        p = urlparse(url)
        return p.scheme in ("http", "https") and bool(p.netloc)

    def _get_ai_client(self) -> "AIClientProtocol | None":
        try:
            from ai.src.clients.gemini_client import GeminiClient

            return GeminiClient()
        except Exception:
            return None

    def _generate_recommendation(
        self,
        issue: str,
        page_context: str,
        client: "AIClientProtocol",
    ) -> str | None:
        try:
            from ai.src.services.recommendation import generate_recommendation

            return generate_recommendation(
                issue=issue,
                page_context=page_context,
                client=client,
            )
        except Exception:
            return None

    def _build_page_context(self, page_data: PageData) -> str:
        context = page_data.text.strip()
        if context:
            return context

        fallback = " ".join(
            [
                page_data.title,
                page_data.meta_description,
                " ".join(page_data.h1_tags),
            ]
        ).strip()
        return fallback

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
        recommendations: list[str] = []

        if seo_result.issues:
            ai_client = self._get_ai_client()
            page_context = self._build_page_context(page_data)

            if ai_client is not None and page_context:
                for issue in seo_result.issues:
                    recommendation = self._generate_recommendation(
                        issue=issue,
                        page_context=page_context,
                        client=ai_client,
                    )
                    if recommendation:
                        recommendations.append(recommendation)

        return AnalyzeResponse(
            url=url,
            seo_score=seo_result.score,
            aeo_score=0,
            issues=seo_result.issues,
            recommendations=recommendations,
        )
