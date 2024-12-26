from .api_openai import OpenAiApiConnection
from .api_anthropic import AnthropicApiConnection
from .api_dummy import DummyApiConnection


API_BY_PROVIDER = {
    'anthropic': AnthropicApiConnection,
    'dummy': DummyApiConnection,
}  # default: OpenAiApiConnection


class Client:
    def __init__(self, model, **kwargs):
        self.model = model
        self.kwargs = kwargs
        self.recorder = None

    def chat(self, messages, model=None, **kwargs):
        # TODO: self.kwargs
        conn = self._get_connection(model, **kwargs)
        return conn.chat(messages, model, **kwargs)

    def chat_stream(self, messages, model=None, **kwargs):
        # TODO: self.kwargs
        conn = self._get_connection(model, **kwargs)
        return conn.chat_stream(messages, model, **kwargs)

    def _get_connection(self, model, **kwargs):
        model = model or self.model
        provider, _, _ = model.partition(":")
        api = API_BY_PROVIDER.get(provider, OpenAiApiConnection)
        conn = api(model, **kwargs)
        conn.recorder = self.recorder
        return conn


def client(model=None, **kwargs):
    return Client(model, **kwargs)
