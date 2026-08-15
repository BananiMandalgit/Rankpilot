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