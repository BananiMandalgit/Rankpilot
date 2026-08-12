from bs4 import BeautifulSoup


def parse_html(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, 'html.parser')
from bs4 import BeautifulSoup

def parse_html(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, 'html.parser')


def extract_seo_data(soup: BeautifulSoup) -> dict:
    """Pull title, meta description, H1s, images, and text from parsed HTML."""

    title = soup.title.string.strip() if soup.title and soup.title.string else ""

    meta_tag = soup.find("meta", attrs={"name": "description"})
    meta_description = meta_tag["content"].strip() if meta_tag and meta_tag.get("content") else ""

    h1_tags = [h1.get_text(strip=True) for h1 in soup.find_all("h1")]

    images = [
        {"src": img.get("src", ""), "alt": img.get("alt", "")}
        for img in soup.find_all("img")
    ]

    for tag in soup(["script", "style"]):
        tag.decompose()
    main_text = soup.get_text(separator=" ", strip=True)

    return {
        "title": title,
        "meta_description": meta_description,
        "h1_tags": h1_tags,
        "images": images,
        "main_text": main_text,
    }