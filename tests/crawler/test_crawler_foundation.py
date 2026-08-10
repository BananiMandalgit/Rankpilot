from pathlib import Path
import sys


CRAWLER_ROOT = Path(__file__).resolve().parents[2] / 'crawler'
if str(CRAWLER_ROOT) not in sys.path:
    sys.path.insert(0, str(CRAWLER_ROOT))

from src.core.config import CrawlerConfig
from src.parsers.html_parser import parse_html
from src.services.crawler_service import CrawlerService


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