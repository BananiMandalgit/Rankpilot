from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CrawlerConfig:
    timeout_seconds: float = 10.0
    user_agent: str = 'RankPilotCrawler/0.1 (+https://example.com)'
    max_pages: int = 100
    respect_robots_txt: bool = True