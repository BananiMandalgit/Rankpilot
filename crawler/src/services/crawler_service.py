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