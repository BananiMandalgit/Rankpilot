from dataclasses import dataclass, field
from bs4 import BeautifulSoup


@dataclass(slots=True)
class PageData:
    url: str
    title: str = ""
    meta_description: str = ""
    h1_tags: list[str] = field(default_factory=list)
    h1_count: int = 0
    images: list[dict] = field(default_factory=list)
    image_count: int = 0
    images_missing_alt: int = 0
    text: str = ""
    word_count: int = 0
    raw_html: str = ""
    status_code: int = 0
    error: str = ""


def parse_html(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, 'html.parser')


def extract_seo_data(soup: BeautifulSoup, url: str, raw_html: str = "") -> PageData:
    """Pull title, meta description, H1s, images, and text from parsed HTML,
    and return it as a structured PageData object."""

    title = soup.title.string.strip() if soup.title and soup.title.string else ""

    meta_tag = soup.find("meta", attrs={"name": "description"})
    meta_description = meta_tag["content"].strip() if meta_tag and meta_tag.get("content") else ""

    h1_tags = [h1.get_text(strip=True) for h1 in soup.find_all("h1")]

    images = [
        {"src": img.get("src", ""), "alt": img.get("alt", "")}
        for img in soup.find_all("img")
    ]
    images_missing_alt = sum(1 for img in images if not img["alt"])

    for tag in soup(["script", "style"]):
        tag.decompose()
    text = soup.get_text(separator=" ", strip=True)
    word_count = len(text.split())

    return PageData(
        url=url,
        title=title,
        meta_description=meta_description,
        h1_tags=h1_tags,
        h1_count=len(h1_tags),
        images=images,
        image_count=len(images),
        images_missing_alt=images_missing_alt,
        text=text,
        word_count=word_count,
        raw_html=raw_html,
    )