# tests/test_aeo_analyzer.py

import sys
import os

# Allow importing from backend/app when running pytest from repo root
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.services.aeo_analyzer import AEOAnalyzer


class FakePageData:
    """Local stand-in for Member 1's PageData until it's published."""
    def __init__(self, text, word_count):
        self.text = text
        self.word_count = word_count


sample_good = FakePageData(
    text=(
        "What is RankPilot?\n"
        "RankPilot is an SEO and AEO analysis tool.\n\n"
        "Frequently Asked Questions\n"
        "How does it work? It crawls a page and scores it.\n"
    ) * 20,
    word_count=350,
)

sample_poor = FakePageData(
    text="Short page with no structure.",
    word_count=6,
)


def test_good_page_scores_high():
    result = AEOAnalyzer().analyze(sample_good)
    assert result.aeo_score >= 60
    assert isinstance(result.issues, list)


def test_poor_page_scores_low():
    result = AEOAnalyzer().analyze(sample_poor)
    assert result.aeo_score <= 40
    assert len(result.issues) >= 2


def test_result_shape_is_stable():
    result = AEOAnalyzer().analyze(sample_poor)
    assert hasattr(result, "aeo_score")
    assert hasattr(result, "issues")
    assert isinstance(result.aeo_score, int)


def test_score_never_negative():
    worst_case = FakePageData(text="x", word_count=0)
    result = AEOAnalyzer().analyze(worst_case)
    assert result.aeo_score >= 0
    # ---------- new tests: enhancement checks ----------

class HtmlPageData(FakePageData):
    """Extends the fixture with a raw_html attribute for the new checks."""
    def __init__(self, text, word_count, raw_html):
        super().__init__(text, word_count)
        self.raw_html = raw_html


sample_with_structured_data = HtmlPageData(
    text=(
        "What is RankPilot?\n"
        "RankPilot is an SEO and AEO analysis tool.\n"
    ) * 30,
    word_count=350,
    raw_html="""
    <html><head>
    <script type="application/ld+json">
    {"@context": "https://schema.org", "@type": "FAQPage"}
    </script>
    <meta property="article:modified_time" content="2026-01-01T00:00:00Z">
    </head><body>
    <time datetime="2026-01-01">Jan 1, 2026</time>
    </body></html>
    """,
)

sample_html_no_signals = HtmlPageData(
    text="Short page with no structure.",
    word_count=6,
    raw_html="<html><body><p>No schema or dates here.</p></body></html>",
)


def test_structured_data_detected_when_present():
    result = AEOAnalyzer().analyze(sample_with_structured_data)
    assert result.structured_data_ok is True
    assert "faqpage" in result.schema_types_found


def test_freshness_signal_detected_when_present():
    result = AEOAnalyzer().analyze(sample_with_structured_data)
    assert result.freshness_signals_ok is True


def test_structured_data_false_when_html_has_no_jsonld():
    result = AEOAnalyzer().analyze(sample_html_no_signals)
    assert result.structured_data_ok is False
    assert result.schema_types_found == []


def test_enhancement_fields_none_when_no_raw_html():
    # sample_good/sample_poor have no raw_html attribute at all
    result = AEOAnalyzer().analyze(sample_good)
    assert result.structured_data_ok is None
    assert result.freshness_signals_ok is None


def test_qa_structure_detected_on_good_page():
    result = AEOAnalyzer().analyze(sample_good)
    assert result.qa_structure_ok is True


def test_qa_structure_false_on_poor_page():
    result = AEOAnalyzer().analyze(sample_poor)
    assert result.qa_structure_ok is False