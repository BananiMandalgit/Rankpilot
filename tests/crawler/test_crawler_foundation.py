from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from crawler.src.core.config import CrawlerConfig
from crawler.src.parsers.html_parser import parse_html
from crawler.src.services.crawler_service import CrawlerService


def test_crawler_config_defaults() -> None:
    config = CrawlerConfig()

    assert config.timeout_seconds == 10.0
    assert config.max_pages == 100
    assert config.respect_robots_txt is True
    assert 'RankPilotCrawler' in config.user_agent


def test_html_parser_parses_small_document() -> None:
    document = parse_html('<html><body><h1>RankPilot</h1></body></html>')

    assert document.h1 is not None
    assert document.h1.text == 'RankPilot'


def test_crawler_service_import_and_instantiation() -> None:
    service = CrawlerService()

    description = service.describe()

    assert description['timeout_seconds'] == 10.0
    assert description['max_pages'] == 100


    # --- New tests for fetch_and_extract() ---

def test_fetch_valid_page_returns_expected_fields() -> None:
    """A working page should return all expected fields with no error."""
    service = CrawlerService()
    result = service.fetch_and_extract("https://example.com")

    assert result.error == ""
    assert result.status_code == 200
    assert isinstance(result.title, str)
    assert isinstance(result.h1_tags, list)
    assert isinstance(result.images, list)
    assert isinstance(result.text, str)
    assert len(result.text) > 0
    assert result.word_count > 0


def test_fetch_invalid_domain_returns_error() -> None:
    """A URL that doesn't resolve should return a PageData with an error, not crash."""
    service = CrawlerService()
    result = service.fetch_and_extract("https://this-domain-does-not-exist-xyz123.com")

    assert result.error != ""


def test_fetch_garbage_input_returns_error() -> None:
    """Non-URL input should fail gracefully with an error message."""
    service = CrawlerService()
    result = service.fetch_and_extract("asdasd")

    assert result.error != ""


def test_image_and_alt_counts_are_consistent() -> None:
    """images_missing_alt should never exceed image_count."""
    service = CrawlerService()
    result = service.fetch_and_extract("https://example.com")

    assert result.error == ""
    assert result.images_missing_alt <= result.image_count
def test_raw_html_is_preserved() -> None:
    """raw_html should contain the original HTML response, not just extracted text."""
    service = CrawlerService()
    result = service.fetch_and_extract("https://example.com")

    assert result.error == ""
    assert result.raw_html != ""
    assert "<html" in result.raw_html.lower()