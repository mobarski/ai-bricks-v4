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
