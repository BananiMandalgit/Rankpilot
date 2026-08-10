from dataclasses import dataclass
from pathlib import Path
import sys


AI_ROOT = Path(__file__).resolve().parents[2] / 'ai'
if str(AI_ROOT) not in sys.path:
    sys.path.insert(0, str(AI_ROOT))

from src.clients.base import AIClientBase, AIClientConfig, AIClientProtocol
from src.prompts.base import PromptTemplate
from src.services.ai_service import AIService


@dataclass
class FakeAIClient(AIClientBase):
    called: bool = False

    def __init__(self) -> None:
        super().__init__(AIClientConfig(provider_name='fake', model_name='test-model'))
        self.called = False

    def generate(self, prompt: str) -> str:
        self.called = True
        return f'generated: {prompt}'


def test_ai_client_abstraction_can_be_used() -> None:
    client = FakeAIClient()

    assert isinstance(client, AIClientBase)
    assert isinstance(client, AIClientProtocol)
    assert client.config.provider_name == 'fake'
    assert client.generate('hello') == 'generated: hello'
    assert client.called is True


def test_prompt_abstraction_renders_simple_value() -> None:
    prompt = PromptTemplate(name='greeting', template='Hello, {name}!', description='Simple greeting prompt')

    assert prompt.render(name='RankPilot') == 'Hello, RankPilot!'


def test_ai_service_can_be_instantiated_without_network_calls() -> None:
    client = FakeAIClient()
    service = AIService()

    assert service.is_configured() is False

    service.configure_client(client)

    assert service.is_configured() is True
    assert service.client is client
    assert client.called is False

    prompt = PromptTemplate(name='status', template='Status: {value}')
    assert service.build_prompt(prompt, value='ready') == 'Status: ready'
    assert client.called is False