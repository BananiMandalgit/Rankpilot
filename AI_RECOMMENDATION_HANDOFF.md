# AI Recommendation Feature Handoff

## Owner
Member 4

## Purpose
This feature generates a short, structured SEO recommendation for a given issue and page context. The current implementation does not analyze pages itself; it only formats the problem into a prompt and sends that prompt to an AI client.

## Architecture
SEO Issue
→ `generate_recommendation()`
→ `SEO_RECOMMENDATION_PROMPT` (`PromptTemplate`)
→ `GeminiClient`
→ Gemini API
→ Explanation / Recommendation / Suggested

The current control flow is implemented in `ai/src/services/recommendation.py`, which validates inputs and renders the prompt from `ai/src/prompts/seo_recommendation.py`. The AI client abstraction is defined in `ai/src/clients/base.py`, and `GeminiClient` in `ai/src/clients/gemini_client.py` is the concrete provider implementation.

## Files Changed
This handoff covers the following existing implementation files:

- `ai/src/services/recommendation.py` - defines `generate_recommendation(issue, page_context, client)` and validates that both inputs are non-empty.
- `ai/src/prompts/seo_recommendation.py` - defines the `SEO_RECOMMENDATION_PROMPT` template with the required Explanation, Recommendation, and Suggested sections.
- `ai/src/clients/base.py` - defines the `AIClientProtocol` interface used by the recommendation service.
- `ai/src/clients/gemini_client.py` - implements the Gemini provider client using `google.genai` and reads `GEMINI_API_KEY`.
- `tests/ai/test_recommendation.py` - verifies prompt rendering, section formatting, and empty-input validation.
- `tests/ai/test_ai_foundation.py` - verifies the AI client abstraction and prompt template foundation.
- `ai/requirements.txt` - declares the `google-genai` dependency required by `GeminiClient`.

This markdown file is the new handoff artifact for the branch.

## Public API
`generate_recommendation(issue, page_context, client)`

Behavior:
- Raises `ValueError` when `issue` is empty or whitespace.
- Raises `ValueError` when `page_context` is empty or whitespace.
- Renders the SEO recommendation prompt with the supplied values.
- Calls `client.generate(prompt)` and returns the generated text.

Parameters:
- `issue`: the SEO problem description.
- `page_context`: the relevant page or content context.
- `client`: any object that satisfies `AIClientProtocol` and exposes `generate(prompt: str) -> str`.

Return value:
- A string response from the configured AI client.

## Gemini Configuration
`GeminiClient` reads `GEMINI_API_KEY` from the environment unless an API key is passed directly to the constructor.

Local setup:
- Set the environment variable before creating `GeminiClient`.
- On Windows PowerShell, a developer can use `setx GEMINI_API_KEY "your-key-here"` for persistence or `$env:GEMINI_API_KEY = "your-key-here"` for the current session.
- The code also supports `GeminiClient(api_key="...")` for explicit injection in tests or local scripts.

Notes:
- Never hardcode or commit an actual key.
- If the key is missing, `GeminiClient` raises `ValueError("GEMINI_API_KEY is not configured.")`.

## Example
Example input:

```python
from ai.src.clients.gemini_client import GeminiClient
from ai.src.services.recommendation import generate_recommendation

client = GeminiClient(api_key="your-local-development-key")
result = generate_recommendation(
    issue="Missing meta description",
    page_context="Sweet Cake Shop homepage with title, hero banner, and product list",
    client=client,
)
```

Representative output:

```text
Explanation:
The page is missing a meta description, so search engines and users do not get a concise summary of the page.

Recommendation:
Add a clear meta description that describes the page and encourages clicks.

Suggested:
Sweet Cake Shop offers fresh cakes, desserts, and custom celebration orders.
```

## Testing
The existing tests for this feature are in `tests/ai/test_recommendation.py` and `tests/ai/test_ai_foundation.py`.

What they cover:
- The issue and page context are both inserted into the rendered prompt.
- The response includes the three expected sections.
- Empty `issue` and empty `page_context` are rejected.
- The AI client abstraction and prompt template can be used without network calls.

Commands to run:

```powershell
python -m pytest -q tests/ai
```

## Current Test Status
Latest recorded test result: `python -m pytest -q tests/crawler tests/seo tests/ai` completed successfully with exit code `0`.

## Integration for Member 6
Member 6 can call the recommendation function from the backend service layer by importing the AI service and injecting a Gemini client instance.

Current pattern:
- Create a `GeminiClient` in backend code after `GEMINI_API_KEY` is available.
- Pass that client into `generate_recommendation(issue, page_context, client)`.
- Keep the call inside a backend service module rather than putting the AI call directly in a route handler.

Example shape:

```python
from ai.src.clients.gemini_client import GeminiClient
from ai.src.services.recommendation import generate_recommendation

client = GeminiClient()
output = generate_recommendation(
    issue="Missing meta description",
    page_context="Homepage content and title",
    client=client,
)
```

Important limitation:
- There is no FastAPI route for this feature yet in `backend/app/api/`.
- Member 6 would need to wire this into a backend service or a future endpoint.

## Important Notes
- The feature only generates a recommendation from an issue and page context; it does not crawl pages or detect SEO issues.
- The output format is a plain text response with the three required sections.
- `GeminiClient` depends on the `google-genai` package and a valid Gemini API key.
- The current repository foundation intentionally excludes a production backend endpoint for recommendation generation.
- No structured JSON schema is enforced on the model output yet.
