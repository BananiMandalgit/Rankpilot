from dataclasses import dataclass, field

from crawler.src.parsers.html_parser import PageData

MIN_CONTENT_WORDS = 300
CHECK_SCORE = 20


@dataclass(slots=True)
class SEOResult:
    score: int
    title_ok: bool
    meta_description_ok: bool
    h1_ok: bool
    images_alt_ok: bool
    content_length_ok: bool
    issues: list[str] = field(default_factory=list)


class SEOAnalyzer:
    """Run deterministic SEO checks against a PageData object."""

    def analyze(self, page_data: PageData) -> SEOResult:
        issues: list[str] = []

        title_ok = self._title_exists(page_data, issues)
        meta_description_ok = self._meta_description_exists(page_data, issues)
        h1_ok = self._h1_exists(page_data, issues)
        images_alt_ok = self._images_have_alt(page_data, issues)
        content_length_ok = self._content_length_ok(page_data, issues)

        passed_checks = sum(
            [title_ok, meta_description_ok, h1_ok, images_alt_ok, content_length_ok]
        )

        return SEOResult(
            score=passed_checks * CHECK_SCORE,
            title_ok=title_ok,
            meta_description_ok=meta_description_ok,
            h1_ok=h1_ok,
            images_alt_ok=images_alt_ok,
            content_length_ok=content_length_ok,
            issues=issues,
        )

    def _title_exists(self, page_data: PageData, issues: list[str]) -> bool:
        if page_data.title.strip():
            return True
        issues.append("Missing title")
        return False

    def _meta_description_exists(self, page_data: PageData, issues: list[str]) -> bool:
        if page_data.meta_description.strip():
            return True
        issues.append("Missing meta description")
        return False

    def _h1_exists(self, page_data: PageData, issues: list[str]) -> bool:
        if page_data.h1_count > 0:
            return True
        issues.append("Missing H1")
        return False

    def _images_have_alt(self, page_data: PageData, issues: list[str]) -> bool:
        if page_data.image_count == 0:
            return True
        if page_data.images_missing_alt == 0:
            return True
        issues.append(f"{page_data.images_missing_alt} images missing ALT")
        return False

    def _content_length_ok(self, page_data: PageData, issues: list[str]) -> bool:
        if page_data.word_count >= MIN_CONTENT_WORDS:
            return True
        issues.append("Content is too short")
        return False
