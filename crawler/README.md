# Crawler
The crawler module fetches a webpage and extracts structured SEO data (title, meta description, headings, images, text, word count). Multi-page crawling, SEO analysis, AEO analysis, and persistence are handled elsewhere or not yet implemented.
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

Single-page fetch and extraction is implemented and tested (`CrawlerService.fetch_and_extract`). Multi-page crawling, link discovery, robots.txt handling, and persistence are not yet implemented — planned for later.

## Usage

Import and call the crawler service to get structured page data:

```python
from crawler.src.services.crawler_service import CrawlerService

page_data = CrawlerService().fetch_and_extract(url)

if page_data.error:
    # crawl failed - handle the error, page_data.error has the reason
    ...
else:
    # crawl succeeded - use these fields:
    page_data.title              # str
    page_data.meta_description   # str
    page_data.h1_count           # int
    page_data.image_count        # int
    page_data.images_missing_alt # int
    page_data.text               # str
    page_data.word_count         # int
    page_data.status_code        # int
```

Always check `page_data.error` first before using the other fields.