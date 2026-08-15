from fastapi.testclient import TestClient
from crawler.src.parsers.html_parser import PageData
from seo.src.seo_analyzer import SEOResult

from app.main import app


client = TestClient(app)


def test_analyze_successful_integration(monkeypatch) -> None:
    def fake_fetch_and_extract(self, url: str) -> PageData:
        return PageData(url=url, title="Title", meta_description="Desc", h1_count=1, word_count=400)

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

    monkeypatch.setattr("crawler.src.services.crawler_service.CrawlerService.fetch_and_extract", fake_fetch_and_extract)
    monkeypatch.setattr("seo.src.seo_analyzer.SEOAnalyzer.analyze", fake_analyze)

    response = client.post('/api/v1/analyze', json={"url": "https://example.com"})

    assert response.status_code == 200
    data = response.json()
    # Pydantic may normalize URLs (trailing slash). Normalize before asserting.
    assert data['url'].rstrip('/') == 'https://example.com'
    assert data['seo_score'] == 80
    assert data['aeo_score'] == 0
    assert data['issues'] == ["Content is too short"]
    assert data['recommendations'] == []


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
