from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@runtime_checkable
class AIClientProtocol(Protocol):
    def generate(self, prompt: str) -> str:
        """Return a generated response for the supplied prompt."""


@dataclass(slots=True)
class AIClientConfig:
    provider_name: str
    model_name: str | None = None


class AIClientBase:
    def __init__(self, config: AIClientConfig) -> None:
        self._config = config

    @property
    def config(self) -> AIClientConfig:
        return self._config

    def generate(self, prompt: str) -> str:
        raise NotImplementedError('AI provider integration is not implemented yet.')