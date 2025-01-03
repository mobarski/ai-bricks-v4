from .api_openai import OpenAiApiConnection


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

    def normalize_request(self, request, ctx):
        messages = request['data']['messages']
        request['data']['messages'] = [self.normalize_message(msg) for msg in messages]
        return request

    def normalize_message(self, msg):
        if isinstance(msg['content'], str):
            return msg
        out = []
        for part in msg['content']:
            if part['type'] == 'text':
                out.append(part)
            elif part['type'] == 'image_url':
                if part['image_url']['url'].startswith('data:'):
                    # example: "data:image/{extension};base64,{image_as_base64}"
                    meta, raw_data = part['image_url']['url'].split(';')
                    media_type = meta.split(':')[-1]
                    data = raw_data.split(',')[-1]
                else:
                    raise NotImplementedError(f"Unsupported image URL: {part['image_url']['url']}")
                part2 = {
                    'type': 'image',
                    'source': {
                        'data': data,
                        'type': 'base64',
                        'media_type': media_type,
                    }
                }
                out.append(part2)
        return {'role': msg['role'], 'content': out}
