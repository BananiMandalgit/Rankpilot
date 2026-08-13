from __future__ import annotations

from ..clients.base import AIClientProtocol
from ..prompts.seo_recommendation import SEO_RECOMMENDATION_PROMPT


def generate_recommendation(
    issue: str,
    page_context: str,
    client: AIClientProtocol,
) -> str:
    """Generate an AI recommendation for an SEO issue."""

    if not issue.strip():
        raise ValueError("SEO issue cannot be empty.")

    if not page_context.strip():
        raise ValueError("Page context cannot be empty.")

    prompt = SEO_RECOMMENDATION_PROMPT.render(
        issue=issue,
        page_context=page_context,
    )

    return client.generate(prompt)