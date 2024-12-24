import json
import os

import requests

from .utils.namespace import DictNamespace
from .config import providers, lookup

# REF: https://github.com/andrewyng/aisuite/blob/main/aisuite/providers/openai_provider.py
# REF:https://platform.openai.com/docs/api-reference/chat/create


class ApiConnection:

    def __init__(self, model, **kwargs):
        super().__init__()
        self.model = model
        self.kwargs = kwargs

    def chat(self, messages, /, model=None, **kwargs):
        request = self.prepare_chat_request(messages, model, **kwargs)
        request = self.preproc_request(request)
        raw_resp = self.post_request(**request)
        resp = self.parse_response(raw_resp)
        resp = self.postproc_response(resp, request)
        return resp

    def chat_stream(self, messages, /, model=None, **kwargs):
        kwargs['stream'] = True
        request = self.prepare_chat_request(messages, model, **kwargs)
        request = self.preproc_request(request)
        raw_resp = self.post_request(**request)
        for line in raw_resp.iter_lines():
            line = line.decode("utf-8").strip()
            if line == "data: [DONE]":
                break
            if line.startswith("data: {"):
                raw_data = line[5:]
                yield self.parse_stream_response(raw_data)

    # -------------------------------------------------------------------------

    def prepare_chat_request(self, messages, model=None, **kwargs):
        # TODO: route to other class based on the provider
        model = model or self.model
        provider, model_name = model.split(":", maxsplit=1)
        return self.build_chat_request(messages, model_name, provider, **kwargs)

    def build_chat_request(self, messages, model_name, provider, **kwargs):
        """build request dictionary for chat completions api call"""
        api_key_env = providers.lookup(f'{provider}.api_key_env')
        api_base_url = providers.lookup(f'{provider}.api_base_url')
        return {
            'url': self.build_chat_url(api_base_url),
            'headers': self.build_headers(api_key_env),
            'data': self.build_request_data(messages, model_name, **kwargs),
        }

    def post_request(self, **kwargs):
        # TODO: handle errors and retries
        kwargs['data'] = json.dumps(kwargs['data'])
        return requests.post(**kwargs)

    def build_chat_url(self, api_base_url):
        return api_base_url + "/chat/completions"

    def build_headers(self, api_key_env):
        api_key = "NO-API-KEY-SET"
        if api_key_env:
            api_key = os.getenv(api_key_env)
            if not api_key:
                raise Exception(f"environment variable {api_key_env} is not set")
        return {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def build_request_data(self, messages, model_name, **kwargs):
        return {
            'model': model_name,
            'messages': messages,
            **{**self.kwargs, **kwargs}
        }

    def parse_response(self, raw_resp) -> DictNamespace:
        """parse response from chat completions api call"""
        try:
            resp = raw_resp.json()
        except json.JSONDecodeError:
            raise Exception(f"Failed to parse response: {raw_resp.text}")
        return DictNamespace(resp)

    def parse_stream_response(self, raw_resp) -> DictNamespace:
        """parse response from chat completions api call"""
        try:
            resp = json.loads(raw_resp)
        except json.JSONDecodeError:
            raise Exception(f"Failed to parse response: {raw_resp.text}")
        return DictNamespace(resp)

    # -------------------------------------------------------------------------

    def preproc_request(self, request):
        return request

    def postproc_response(self, response, request=None):
        return response


if __name__ == "__main__":
    conn = ApiConnection("openai:gpt-4o")
    if True:
        resp = conn.chat([{"role": "user", "content": "Tell me a joke."}])
        print(resp)
        resp = conn.chat([{"role": "user", "content": "Tell me a joke."}], model="xai:grok-beta")
        print(resp)
    if True:
        for chunk in conn.chat_stream([{"role": "user", "content": "Tell me a joke."}]):
            #print(lookup(chunk, 'choices.0.delta.content', ''), end="", flush=True)
            print(chunk)
        print()
