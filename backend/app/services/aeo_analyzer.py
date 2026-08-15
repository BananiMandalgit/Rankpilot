# backend/app/services/aeo_analyzer.py

from app.schemas.aeo import AEOResult

# If Member 1 has published PageData as a schema, import it instead:
# from app.schemas.page_data import PageData

MIN_WORD_COUNT = 300
QUESTION_STARTERS = ("what", "why", "how", "when", "where", "who", "which")
FAQ_KEYWORDS = ("faq", "frequently asked questions", "q&a", "questions and answers")


class AEOAnalyzer:
    """
    Deterministic AEO analyzer.
    Input:  PageData
    Output: AEOResult

    No LLM, no external API calls, no database, no NLP libraries.
    Four fixed, explainable checks only.
    """

    def analyze(self, page_data) -> AEOResult:
        issues = []
        score = 100

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

        return AEOResult(aeo_score=max(score, 0), issues=issues)

    # ---------- individual checks ----------

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