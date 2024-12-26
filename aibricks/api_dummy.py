from .api_openai import OpenAiApiConnection


class DummyApiConnection(OpenAiApiConnection):

    def post_request(self, **kwargs):
        return {}

    def parse_response(self, raw_resp) -> dict:
        return raw_resp

    def parse_stream_response(self, raw_resp) -> dict:
        return raw_resp


if __name__ == "__main__":
    conn = DummyApiConnection("dummy:xxx", max_tokens=100)
    resp = conn.chat([{"role": "user", "content": "Tell me a joke."}])
    print(resp)
