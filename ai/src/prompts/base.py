from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class PromptTemplate:
    name: str
    template: str
    description: str = ''
    metadata: dict[str, str] = field(default_factory=dict)

    def render(self, **values: str) -> str:
        return self.template.format(**values)