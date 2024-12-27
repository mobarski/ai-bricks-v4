from . import common

TEST_MODEL = "openai:gpt-4o-mini"


def test_chat():
    common.test_chat(TEST_MODEL)


def test_chat_stream():
    common.test_chat_stream(TEST_MODEL)


if __name__ == "__main__":
    test_chat()
    test_chat_stream()
