from dataclasses import dataclass, field

from ..core.config import CrawlerConfig


@dataclass(slots=True)
class CrawlerService:
    config: CrawlerConfig = field(default_factory=CrawlerConfig)

    def describe(self) -> dict[str, str | int | float | bool]:
        return {
            'timeout_seconds': self.config.timeout_seconds,
            'user_agent': self.config.user_agent,
            'max_pages': self.config.max_pages,
            'respect_robots_txt': self.config.respect_robots_txt,
        }
    from dataclasses import dataclass, field
import requests
from ..core.config import CrawlerConfig
from ..parsers.html_parser import parse_html, extract_seo_data


@dataclass(slots=True)
class CrawlerService:
    config: CrawlerConfig = field(default_factory=CrawlerConfig)

    def describe(self) -> dict[str, str | int | float | bool]:
        return {
            'timeout_seconds': self.config.timeout_seconds,
            'user_agent': self.config.user_agent,
            'max_pages': self.config.max_pages,
            'respect_robots_txt': self.config.respect_robots_txt,
        }

    def fetch_and_extract(self, url: str) -> dict:
        """Fetch a single page and return extracted SEO data, or an error."""
        try:
            response = requests.get(
                url,
                timeout=self.config.timeout_seconds,
                headers={"User-Agent": self.config.user_agent},
            )
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return {"error": f"Could not fetch page: {str(e)}"}

        soup = parse_html(response.text)
        data = extract_seo_data(soup)
        data["url"] = url
        data["status_code"] = response.status_code
        return data