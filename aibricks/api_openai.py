import json
import os

import requests

from .config import providers
from .utils.image import image_as_url

# REF: https://github.com/andrewyng/aisuite/blob/main/aisuite/providers/openai_provider.py
# REF:https://platform.openai.com/docs/api-reference/chat/create


class OpenAiApiConnection:
    stream_kwargs = {
        'stream': True,
        'stream_options': {"include_usage": True},
    }

    def __init__(self, model, **kwargs):
        super().__init__()
        self.model = model
        self.kwargs = kwargs
        self.recorder = None

    def chat(self, messages, model=None, **kwargs):
        ctx = {}
        request = self.prepare_chat_request(messages, model, ctx, **kwargs)
        request = self.preproc_request(request, ctx=ctx)
        raw_resp = self.post_request(**request)
        resp = self.parse_response(raw_resp)
        resp = self.postproc_response(resp, ctx=ctx)
        return resp

    def chat_stream(self, messages, model=None, **kwargs):
        ctx = {}
        kwargs = {**self.stream_kwargs, **kwargs}
        request = self.prepare_chat_request(messages, model, ctx, **kwargs)
        request = self.preproc_request(request, ctx=ctx)
        raw_resp = self.post_request(**request)
        for line in raw_resp.iter_lines():
            line = line.decode("utf-8").strip()
            if line.startswith("data: {"):
                raw_data = line[5:]
                chunk = self.parse_stream_response(raw_data)
                chunk = self.postproc_stream_response(chunk, ctx=ctx)
                if chunk:
                    yield chunk

    # -------------------------------------------------------------------------

    def prepare_chat_request(self, messages, model, ctx, **kwargs):
        # TODO: route to other class based on the provider
        model = model or self.model
        ctx['model'] = model
        provider, _, model_name = model.partition(":")
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
        api_key = self.get_api_key(api_key_env)
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

    def parse_response(self, raw_resp) -> dict:
        """parse response from chat completions api call"""
        try:
            resp = raw_resp.json()
        except json.JSONDecodeError:
            raise Exception(f"Failed to parse response: {raw_resp.text}")
        return resp

    def parse_stream_response(self, raw_resp) -> dict:
        try:
            resp = json.loads(raw_resp)
        except json.JSONDecodeError:
            raise Exception(f"Failed to parse response: {raw_resp}")
        return resp

    def get_api_key(self, api_key_env):
        """Retrieve API key from environment variable"""
        if not api_key_env:
            return "NO-API-KEY-SET"

        api_key = os.getenv(api_key_env)
        if not api_key:
            raise Exception(f"environment variable {api_key_env} is not set")
        return api_key

    # -------------------------------------------------------------------------

    def preproc_request(self, request, ctx):
        if self.recorder:
            self.recorder.record_request(request, ctx)
        request = self.normalize_request(request, ctx)
        return request

    def postproc_response(self, response, ctx):
        if self.recorder:
            self.recorder.record_response(response, ctx)
        response = self.normalize_response(response, ctx)
        return response

    def postproc_stream_response(self, response, ctx):
        if self.recorder:
            self.recorder.record_stream_response(response, ctx)
        response = self.normalize_stream_response(response, ctx)
        return response

    # -------------------------------------------------------------------------

    def normalize_request(self, request, ctx):
        messages = request['data']['messages']
        request['data']['messages'] = [self.normalize_message(msg, ctx) for msg in messages]
        return request

    def normalize_message(self, msg, ctx):
        if isinstance(msg['content'], str):
            return msg
        elif isinstance(msg['content'], list):
            msg['content'] = [self.normalize_content_part(part, ctx) for part in msg['content']]
        else:
            raise ValueError(f"Unsupported message content type: {type(msg['content'])}")
        return msg

    def normalize_content_part(self, part, ctx):
        if part['type'] == 'image_url':
            url = part['image_url']['url']
            if url.startswith('file://') or url.startswith('http'):
                part['image_url']['url'] = image_as_url(url)
        elif part['type'] == 'image':
            image = part.pop('image')
            part['type'] = 'image_url'
            part['image_url'] = {'url': image_as_url(image)}
        return part

    # -------------------------------------------------------------------------

    def normalize_response(self, response, ctx):
        return response

    def normalize_stream_response(self, response, ctx):
        return response
