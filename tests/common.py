import aibricks


def test_chat(model):
    conn = aibricks.client(model)
    resp = conn.chat([{"role": "user", "content": "Tell me a joke."}])
    print(resp)


def test_chat_stream(model):
    conn = aibricks.client(model)
    for chunk in conn.chat_stream([{"role": "user", "content": "Tell me a joke."}]):
        print(chunk)
