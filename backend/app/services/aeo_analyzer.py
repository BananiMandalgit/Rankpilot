# backend/app/services/aeo_analyzer.py

import json
import re

from app.schemas.aeo import AEOResult

# If Member 1 has published PageData as a schema, import it instead:
# from app.schemas.page_data import PageData

MIN_WORD_COUNT = 300
QUESTION_STARTERS = ("what", "why", "how", "when", "where", "who", "which")
FAQ_KEYWORDS = ("faq", "frequently asked questions", "q&a", "questions and answers")

KNOWN_SCHEMA_TYPES = {"webpage", "article", "faqpage", "howto"}
JSONLD_PATTERN = re.compile(
    r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.IGNORECASE | re.DOTALL,
)
FRESHNESS_PATTERNS = (
    re.compile(r"datemodified", re.IGNORECASE),
    re.compile(r"article:modified_time", re.IGNORECASE),
    re.compile(r"<time[^>]+datetime", re.IGNORECASE),
)


class AEOAnalyzer:
    """
    Deterministic AEO analyzer.
    Input:  PageData
    Output: AEOResult

    No LLM, no external API calls, no database, no NLP libraries.
    """

    def analyze(self, page_data) -> AEOResult:
        issues = []
        score = 100

        # ---------- original 4 checks (unchanged) ----------
        if not self._has_useful_headings(page_data.text):
            score -= 20
            issues.append("No clear heading structure detected")

        if not self._has_question_like_content(page_data.text):
            score -= 20
            issues.append("No question-like headings or content detected")

        if not self._has_enough_content(page_data.word_count):
            score -= 20
            issues.append(
                f"Content is short ({page_data.word_count} words, recommend 300+)"
            )

        if not self._has_faq_signal(page_data.text):
            score -= 20
            issues.append("No FAQ/Q&A signals detected")

        # ---------- enhancement: Question -> Answer structure ----------
        # Uses .text, which is always available. Small penalty by design
        # so it doesn't overwhelm the original 4-check scoring.
        qa_structure_ok = self._has_question_answer_structure(page_data.text)
        if not qa_structure_ok:
            score -= 5
            issues.append("No question-heading followed by an answer detected")

        # ---------- enhancements: JSON-LD + freshness (need raw HTML) ----------
        # PageData does not yet expose raw HTML. These checks safely no-op
        # (None, no penalty) until that field exists, instead of guessing.
        raw_html = getattr(page_data, "raw_html", "") or ""

        structured_data_ok = None
        schema_types_found = []
        freshness_signals_ok = None

        if raw_html:
            structured_data_ok, schema_types_found = self._detect_structured_data(raw_html)
            if not structured_data_ok:
                score -= 5
                issues.append(
                    "No structured data (JSON-LD) detected "
                    "(WebPage/Article/FAQPage/HowTo)"
                )

            freshness_signals_ok = self._has_freshness_signals(raw_html)
            if not freshness_signals_ok:
                score -= 5
                issues.append(
                    "No freshness signals detected "
                    "(dateModified / article:modified_time / <time datetime>)"
                )

        return AEOResult(
            aeo_score=max(score, 0),
            issues=issues,
            structured_data_ok=structured_data_ok,
            schema_types_found=schema_types_found,
            qa_structure_ok=qa_structure_ok,
            freshness_signals_ok=freshness_signals_ok,
        )

    # ---------- individual checks (original 4, unchanged) ----------

    def _has_useful_headings(self, text: str) -> bool:
        lines = [l.strip() for l in text.split("\n") if l.strip()]
        heading_like = [
            l for l in lines if len(l.split()) <= 8 and l[0:1].isupper()
        ]
        return len(heading_like) >= 2

    def _has_question_like_content(self, text: str) -> bool:
        lowered = text.lower()
        has_question_mark = "?" in text
        has_question_word = any(
            lowered.strip().startswith(q) or f" {q} " in lowered
            for q in QUESTION_STARTERS
        )
        return has_question_mark or has_question_word

    def _has_enough_content(self, word_count: int) -> bool:
        return word_count >= MIN_WORD_COUNT

    def _has_faq_signal(self, text: str) -> bool:
        lowered = text.lower()
        return any(keyword in lowered for keyword in FAQ_KEYWORDS)

    # ---------- new: Question -> Answer structure ----------

    def _has_question_answer_structure(self, text: str) -> bool:
        """
        Looks for a short question-style line, followed within 2 lines
        by a non-empty line acting as the answer.
        """
        lines = [l.strip() for l in text.split("\n")]
        for i, line in enumerate(lines):
            if line.endswith("?") and 1 <= len(line.split()) <= 12:
                for j in range(i + 1, min(i + 3, len(lines))):
                    if lines[j].strip():
                        return True
        return False

    # ---------- new: JSON-LD / structured data ----------

    def _detect_structured_data(self, raw_html: str):
        """
        Returns (found: bool, matched_types: list[str]).
        Looks for <script type="application/ld+json"> blocks and
        checks their @type (or @graph[].@type) against known types.
        """
        matches = JSONLD_PATTERN.findall(raw_html)
        if not matches:
            return False, []

        found_types = set()
        for block in matches:
            try:
                data = json.loads(block.strip())
            except (json.JSONDecodeError, ValueError):
                continue

            candidates = data if isinstance(data, list) else [data]
            for item in candidates:
                if not isinstance(item, dict):
                    continue
                self._collect_type(item.get("@type"), found_types)
                graph = item.get("@graph")
                if isinstance(graph, list):
                    for g in graph:
                        if isinstance(g, dict):
                            self._collect_type(g.get("@type"), found_types)

        matched_known = found_types & KNOWN_SCHEMA_TYPES
        return (len(matched_known) > 0), sorted(matched_known)

    def _collect_type(self, type_value, found_types: set):
        if isinstance(type_value, list):
            found_types.update(str(t).lower() for t in type_value)
        elif type_value:
            found_types.add(str(type_value).lower())

    # ---------- new: freshness signals ----------

    def _has_freshness_signals(self, raw_html: str) -> bool:
        return any(pattern.search(raw_html) for pattern in FRESHNESS_PATTERNS)