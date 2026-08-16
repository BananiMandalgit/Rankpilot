from ai.src.services.recommendation import generate_recommendation


class FakeAIClient:
    def __init__(self) -> None:
        self.received_prompt = ""

    def generate(self, prompt: str) -> str:
        self.received_prompt = prompt
        return """Explanation:
The page does not have a meta description.

Recommendation:
Add a concise description summarizing the page.

Suggested:
Sweet Cake Shop offers delicious cakes and desserts."""


def test_generate_recommendation_uses_issue_and_page_context() -> None:
    client = FakeAIClient()

    result = generate_recommendation(
        issue="Missing meta description",
        page_context="Sweet Cake Shop",
        client=client,
    )

    assert "Missing meta description" in client.received_prompt
    assert "Sweet Cake Shop" in client.received_prompt
    assert "Explanation:" in result
    assert "Recommendation:" in result
    assert "Suggested:" in result


def test_generate_recommendation_rejects_empty_issue() -> None:
    client = FakeAIClient()

    try:
        generate_recommendation(
            issue="",
            page_context="Sweet Cake Shop",
            client=client,
        )
        assert False, "Expected ValueError"
    except ValueError as error:
        assert str(error) == "SEO issue cannot be empty."


def test_generate_recommendation_rejects_empty_page_context() -> None:
    client = FakeAIClient()

    try:
        generate_recommendation(
            issue="Missing meta description",
            page_context="",
            client=client,
        )
        assert False, "Expected ValueError"
    except ValueError as error:
        assert str(error) == "Page context cannot be empty."