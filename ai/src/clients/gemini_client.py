from __future__ import annotations

import os

from google import genai

from .base import AIClientBase, AIClientConfig


class GeminiClient(AIClientBase):
    def __init__(
        self,
        api_key: str | None = None,
        model_name: str = "gemini-3.1-flash-lite",
    ) -> None:
        config = AIClientConfig(
            provider_name="gemini",
            model_name=model_name,
        )
        super().__init__(config)

        key = api_key or os.getenv("GEMINI_API_KEY")
        if not key:
            raise ValueError("GEMINI_API_KEY is not configured.")

        self._client = genai.Client(api_key=key)

    def generate(self, prompt: str) -> str:
        response = self._client.models.generate_content(
            model=self.config.model_name,
            contents=prompt,
        )

        if not response.text:
            raise RuntimeError("Gemini returned an empty response.")

        return response.text