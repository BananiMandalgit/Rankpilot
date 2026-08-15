from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from crawler.src.parsers.html_parser import PageData
from seo.src.seo_analyzer import MIN_CONTENT_WORDS, SEOAnalyzer


def build_page_data(**overrides: object) -> PageData:
    base = {
        "url": "https://example.com",
        "title": "Example Title",
        "meta_description": "This is an example meta description.",
        "h1_tags": ["Example Heading"],
        "h1_count": 1,
        "images": [{"src": "/img.jpg", "alt": "Example image"}],
        "image_count": 1,
        "images_missing_alt": 0,
        "text": "word " * MIN_CONTENT_WORDS,
        "word_count": MIN_CONTENT_WORDS,
        "status_code": 200,
        "error": "",
    }
    base.update(overrides)
    return PageData(**base)


def test_all_checks_pass_score_is_100() -> None:
    analyzer = SEOAnalyzer()

    result = analyzer.analyze(build_page_data())

    assert result.score == 100
    assert result.title_ok is True
    assert result.meta_description_ok is True
    assert result.h1_ok is True
    assert result.images_alt_ok is True
    assert result.content_length_ok is True
    assert result.issues == []


def test_missing_title_fails_and_scores_80() -> None:
    analyzer = SEOAnalyzer()

    result = analyzer.analyze(build_page_data(title=""))

    assert result.score == 80
    assert result.title_ok is False
    assert "Missing title" in result.issues


def test_missing_meta_description_fails_and_scores_80() -> None:
    analyzer = SEOAnalyzer()

    result = analyzer.analyze(build_page_data(meta_description=""))

    assert result.score == 80
    assert result.meta_description_ok is False
    assert "Missing meta description" in result.issues


def test_missing_h1_fails_and_scores_80() -> None:
    analyzer = SEOAnalyzer()

    result = analyzer.analyze(build_page_data(h1_tags=[], h1_count=0))

    assert result.score == 80
    assert result.h1_ok is False
    assert "Missing H1" in result.issues


def test_images_missing_alt_fails_and_scores_80() -> None:
    analyzer = SEOAnalyzer()

    result = analyzer.analyze(build_page_data(images_missing_alt=2, image_count=3))

    assert result.score == 80
    assert result.images_alt_ok is False
    assert "2 images missing ALT" in result.issues


def test_content_below_threshold_fails_and_scores_80() -> None:
    analyzer = SEOAnalyzer()

    result = analyzer.analyze(build_page_data(word_count=MIN_CONTENT_WORDS - 1))

    assert result.score == 80
    assert result.content_length_ok is False
    assert "Content is too short" in result.issues


def test_multiple_failures_score_is_calculated_correctly() -> None:
    analyzer = SEOAnalyzer()

    result = analyzer.analyze(
        build_page_data(
            title="",
            meta_description="",
            h1_count=0,
            h1_tags=[],
            images_missing_alt=1,
            image_count=1,
            word_count=MIN_CONTENT_WORDS - 100,
        )
    )

    assert result.score == 0
    assert len(result.issues) == 5


def test_no_images_passes_images_alt_check() -> None:
    analyzer = SEOAnalyzer()

    result = analyzer.analyze(build_page_data(images=[], image_count=0, images_missing_alt=0))

    assert result.images_alt_ok is True
    assert "images missing ALT" not in " ".join(result.issues)


def test_whitespace_only_title_and_meta_description_fail() -> None:
    analyzer = SEOAnalyzer()

    result = analyzer.analyze(build_page_data(title="   ", meta_description="\n\t "))

    assert result.score == 60
    assert result.title_ok is False
    assert result.meta_description_ok is False
    assert "Missing title" in result.issues
    assert "Missing meta description" in result.issues
