from .api_openai import OpenAiApiConnection
from .utils.image import image_as_base64, guess_mime_type
from time import time


class AnthropicApiConnection(OpenAiApiConnection):
    stream_kwargs = {
        'stream': True,
    }

    def build_chat_url(self, api_base_url):
        return api_base_url + "/messages"

    def build_headers(self, api_key_env):
        api_key = self.get_api_key(api_key_env)
        return {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }

    # -------------------------------------------------------------------------

    def normalize_content_part(self, part, ctx):
        if part['type'] == 'image_url':
            url = part['image_url']['url']
            if url.startswith('file://') or url.startswith('http'):
                data = image_as_base64(url)
                media_type = guess_mime_type(url)
            elif url.startswith('data:'):
                # example: "data:{media_type};base64,{image_as_base64}"
                meta, raw_data = url.split(';')
                media_type = meta.split(':')[-1]
                data = raw_data.split(',')[-1]
            return {
                'type': 'image',
                'source': {
                    'data': data,
                    'type': 'base64',
                    'media_type': media_type,
                }
            }
        return part

    def normalize_response(self, response, ctx):
        "transform response into OpenAI format"
        orig = response
        resp = {}
        resp['id'] = orig['id']
        resp['object'] = 'chat.completion'
        resp['created'] = int(time())  # NOT perfect but good enough
        resp['model'] = orig['model']
        resp['choices'] = []
        for i, part in enumerate(orig['content']):
            resp['choices'].append({
                'index': i,
                'message': {
                    'role': orig['role'],
                    'content': part['text'],
                    'refusal': None,
                },
                'finish_reason': self.normalize_finish_reason(orig['stop_reason'], ctx),
            })
        resp['usage'] = self.normalize_usage(orig['usage'], ctx)
        #resp['system_fingerprint'] = 'TODO'  # TODO: what to put here?
        return resp

    def normalize_usage(self, usage, ctx):
        "transform usage into OpenAI format"
        return {
            'prompt_tokens': usage['input_tokens'],
            'completion_tokens': usage['output_tokens'],
            'total_tokens': usage['input_tokens'] + usage['output_tokens'],
        }

    def normalize_finish_reason(self, reason, ctx):
        "map finish reason into OpenAI format"
        return {
            'end_turn': 'stop',
        }.get(reason, reason)

    def normalize_stream_response(self, response, ctx) -> dict:
        part = response
        if part['type'] == 'message_start':
            ctx['stream_id'] = part['message']['id']
            ctx['stream_role'] = part['message']['role']
            ctx['stream_model'] = part['message']['model']
            ctx['stream_usage_input_tokens'] = part['message']['usage']['input_tokens']
            return None
        if part['type'] == 'content_block_start':
            text = part['content_block']['text']
            return self.normalized_stream_part(text, ctx)
        if part['type'] == 'content_block_delta':
            text = part['delta']['text']
            return self.normalized_stream_part(text, ctx)
        if part['type'] == 'message_delta':
            ctx['stream_stop_reason'] = part['delta']['stop_reason']
            finish_reason = self.normalize_finish_reason(ctx['stream_stop_reason'], ctx)
            ctx['stream_usage_output_tokens'] = part['usage']['output_tokens']
            last_part = self.normalized_stream_part('', ctx)
            last_part['choices'] = []
            last_part['usage'] = {
                'prompt_tokens': ctx['stream_usage_input_tokens'],
                'completion_tokens': ctx['stream_usage_output_tokens'],
                'total_tokens': ctx['stream_usage_input_tokens'] + ctx['stream_usage_output_tokens'],
            }
            return last_part

    def normalized_stream_part(self, text, ctx):
        return {
            'id': ctx['stream_id'],
            'object': 'chat.completion.chunk',
            'created': int(time()),
            'model': ctx['stream_model'],
            #'service_tier': 'default',
            #'system_fingerprint': 'TODO',
            'choices': [{
                'index': 0,
                'delta': {'content': text},
                'logprobs': None, # TODO
                'finish_reason': None,
            }],
            'usage': None,
        }
