# Crawler

The crawler module is the future boundary for RankPilot website fetching and page extraction. It is intentionally minimal in this branch and does not perform any real crawling, SEO analysis, AEO analysis, or persistence yet.

## Current Structure

- `crawler/src/core/` - crawler configuration and shared settings
- `crawler/src/parsers/` - HTML parsing helpers
- `crawler/src/services/` - crawler service boundary for later implementation

## Dependencies

- Playwright
- BeautifulSoup4
- httpx
- pytest

## Status

This package only provides the foundation for future crawler work. Actual crawling logic, link discovery, robots handling, and analysis will be implemented later.