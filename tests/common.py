import aibricks


def test_chat(model, **kwargs):
    conn = aibricks.client(model)  # TODO: add kwargs here (but it doesn't work)
    resp = conn.chat([{"role": "user", "content": "Tell me a joke."}], **kwargs)
    print(resp)


def test_chat_stream(model, **kwargs):
    conn = aibricks.client(model)  # TODO: add kwargs here (but it doesn't work)
    for chunk in conn.chat_stream([{"role": "user", "content": "Tell me a joke."}], **kwargs):
        print(chunk)
