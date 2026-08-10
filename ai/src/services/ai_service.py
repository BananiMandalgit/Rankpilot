from __future__ import annotations

from dataclasses import dataclass

from ..clients.base import AIClientProtocol
from ..prompts.base import PromptTemplate


@dataclass(slots=True)
class AIService:
    client: AIClientProtocol | None = None

    def configure_client(self, client: AIClientProtocol) -> None:
        self.client = client

    def build_prompt(self, prompt: PromptTemplate, **values: str) -> str:
        return prompt.render(**values)

    def is_configured(self) -> bool:
        return self.client is not None