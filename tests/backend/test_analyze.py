from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_analyze_successful_placeholder() -> None:
    response = client.post('/api/v1/analyze', json={"url": "https://example.com"})

    assert response.status_code == 200
    data = response.json()
    # Pydantic may normalize URLs (trailing slash). Normalize before asserting.
    assert data['url'].rstrip('/') == 'https://example.com'
    assert data['seo_score'] == 0
    assert data['aeo_score'] == 0
    assert isinstance(data['issues'], list)
    assert isinstance(data['recommendations'], list)


def test_analyze_invalid_url_rejected() -> None:
    response = client.post('/api/v1/analyze', json={"url": "not-a-url"})

    assert response.status_code == 422


def test_analyze_requires_url_field() -> None:
    response = client.post('/api/v1/analyze', json={})

    assert response.status_code == 422
