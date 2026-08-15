from fastapi.testclient import TestClient
from app.schemas.aeo import AEOResult
from crawler.src.parsers.html_parser import PageData
from seo.src.seo_analyzer import SEOResult

from app.main import app


client = TestClient(app)


class FakeAIClient:
    def generate(self, prompt: str) -> str:
        return f"AI recommendation for: {prompt[:20]}"


def test_analyze_successful_integration(monkeypatch) -> None:
    def fake_fetch_and_extract(self, url: str) -> PageData:
        return PageData(
            url=url,
            title="Title",
            meta_description="Desc",
            h1_count=1,
            word_count=400,
            text="Sample page content for AI context.",
        )

    def fake_analyze(self, page_data: PageData) -> SEOResult:
        return SEOResult(
            score=80,
            title_ok=True,
            meta_description_ok=True,
            h1_ok=True,
            images_alt_ok=True,
            content_length_ok=False,
            issues=["Content is too short"],
        )

    def fake_generate_recommendation(self, issue: str, page_context: str, client) -> str:
        return f"Fix: {issue}"

    def fake_aeo_analyze(self, page_data: PageData) -> AEOResult:
        return AEOResult(aeo_score=65, issues=["No FAQ/Q&A signals detected"])

    monkeypatch.setattr("app.services.analysis.AnalysisService._get_ai_client", lambda self: FakeAIClient())
    monkeypatch.setattr("app.services.analysis.AnalysisService._generate_recommendation", fake_generate_recommendation)

    monkeypatch.setattr("crawler.src.services.crawler_service.CrawlerService.fetch_and_extract", fake_fetch_and_extract)
    monkeypatch.setattr("seo.src.seo_analyzer.SEOAnalyzer.analyze", fake_analyze)
    monkeypatch.setattr("app.services.aeo_analyzer.AEOAnalyzer.analyze", fake_aeo_analyze)

    response = client.post('/api/v1/analyze', json={"url": "https://example.com"})

    assert response.status_code == 200
    data = response.json()
    # Pydantic may normalize URLs (trailing slash). Normalize before asserting.
    assert data['url'].rstrip('/') == 'https://example.com'
    assert data['seo_score'] == 80
    assert data['aeo_score'] == 65
    assert data['issues'] == ["Content is too short"]
    assert data['recommendations'] == ["Fix: Content is too short"]


def test_analyze_no_seo_issues_returns_empty_recommendations(monkeypatch) -> None:
    def fake_fetch_and_extract(self, url: str) -> PageData:
        return PageData(url=url, title="Title", meta_description="Desc", h1_count=1, word_count=600, text="Long enough content")

    def fake_analyze(self, page_data: PageData) -> SEOResult:
        return SEOResult(
            score=100,
            title_ok=True,
            meta_description_ok=True,
            h1_ok=True,
            images_alt_ok=True,
            content_length_ok=True,
            issues=[],
        )

    def fake_aeo_analyze(self, page_data: PageData) -> AEOResult:
        return AEOResult(aeo_score=90, issues=[])

    monkeypatch.setattr("crawler.src.services.crawler_service.CrawlerService.fetch_and_extract", fake_fetch_and_extract)
    monkeypatch.setattr("seo.src.seo_analyzer.SEOAnalyzer.analyze", fake_analyze)
    monkeypatch.setattr("app.services.aeo_analyzer.AEOAnalyzer.analyze", fake_aeo_analyze)

    response = client.post('/api/v1/analyze', json={"url": "https://example.com"})

    assert response.status_code == 200
    data = response.json()
    assert data['seo_score'] == 100
    assert data['aeo_score'] == 90
    assert data['issues'] == []
    assert data['recommendations'] == []


def test_analyze_handles_unconfigured_gemini_client_safely(monkeypatch) -> None:
    def fake_fetch_and_extract(self, url: str) -> PageData:
        return PageData(url=url, title="Title", meta_description="Desc", h1_count=1, word_count=400, text="Context")

    def fake_analyze(self, page_data: PageData) -> SEOResult:
        return SEOResult(
            score=80,
            title_ok=True,
            meta_description_ok=True,
            h1_ok=True,
            images_alt_ok=True,
            content_length_ok=False,
            issues=["Content is too short"],
        )

    def fake_aeo_analyze(self, page_data: PageData) -> AEOResult:
        return AEOResult(aeo_score=70, issues=["No FAQ/Q&A signals detected"])

    monkeypatch.setattr("crawler.src.services.crawler_service.CrawlerService.fetch_and_extract", fake_fetch_and_extract)
    monkeypatch.setattr("seo.src.seo_analyzer.SEOAnalyzer.analyze", fake_analyze)
    monkeypatch.setattr("app.services.aeo_analyzer.AEOAnalyzer.analyze", fake_aeo_analyze)
    monkeypatch.setattr("app.services.analysis.AnalysisService._get_ai_client", lambda self: None)

    response = client.post('/api/v1/analyze', json={"url": "https://example.com"})

    assert response.status_code == 200
    data = response.json()
    assert data['seo_score'] == 80
    assert data['aeo_score'] == 70
    assert data['issues'] == ["Content is too short"]
    assert data['recommendations'] == []


def test_analyze_passes_same_page_data_to_seo_and_aeo(monkeypatch) -> None:
    captured: dict[str, PageData] = {}

    def fake_fetch_and_extract(self, url: str) -> PageData:
        return PageData(url=url, title="Title", meta_description="Desc", h1_count=1, word_count=500, text="FAQ content?")

    def fake_seo_analyze(self, page_data: PageData) -> SEOResult:
        captured['seo'] = page_data
        return SEOResult(
            score=100,
            title_ok=True,
            meta_description_ok=True,
            h1_ok=True,
            images_alt_ok=True,
            content_length_ok=True,
            issues=[],
        )

    def fake_aeo_analyze(self, page_data: PageData) -> AEOResult:
        captured['aeo'] = page_data
        return AEOResult(aeo_score=85, issues=[])

    monkeypatch.setattr("crawler.src.services.crawler_service.CrawlerService.fetch_and_extract", fake_fetch_and_extract)
    monkeypatch.setattr("seo.src.seo_analyzer.SEOAnalyzer.analyze", fake_seo_analyze)
    monkeypatch.setattr("app.services.aeo_analyzer.AEOAnalyzer.analyze", fake_aeo_analyze)

    response = client.post('/api/v1/analyze', json={"url": "https://example.com"})

    assert response.status_code == 200
    assert captured['seo'] is captured['aeo']
    assert response.json()['aeo_score'] == 85


def test_analyze_handles_crawler_error_safely(monkeypatch) -> None:
    def fake_fetch_and_extract(self, url: str) -> PageData:
        raise RuntimeError("network down")

    monkeypatch.setattr("crawler.src.services.crawler_service.CrawlerService.fetch_and_extract", fake_fetch_and_extract)

    response = client.post('/api/v1/analyze', json={"url": "https://example.com"})

    assert response.status_code == 200
    data = response.json()
    assert data['seo_score'] == 0
    assert data['aeo_score'] == 0
    assert data['issues'] == ["Crawler error: network down"]
    assert data['recommendations'] == []


def test_analyze_uses_crawler_error_response(monkeypatch) -> None:
    def fake_fetch_and_extract(self, url: str) -> PageData:
        return PageData(url=url, error="Could not fetch page: timeout")

    monkeypatch.setattr("crawler.src.services.crawler_service.CrawlerService.fetch_and_extract", fake_fetch_and_extract)

    response = client.post('/api/v1/analyze', json={"url": "https://example.com"})

    assert response.status_code == 200
    data = response.json()
    assert data['seo_score'] == 0
    assert data['issues'] == ["Could not fetch page: timeout"]


def test_analyze_invalid_url_rejected() -> None:
    response = client.post('/api/v1/analyze', json={"url": "not-a-url"})

    assert response.status_code == 422


def test_analyze_requires_url_field() -> None:
    response = client.post('/api/v1/analyze', json={})

    assert response.status_code == 422
