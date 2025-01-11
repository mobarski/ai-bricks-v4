from . import common

TEST_MODEL = "deepseek:deepseek-chat"


def test_chat():
    common.test_chat(TEST_MODEL)


def test_chat_stream():
    common.test_chat_stream(TEST_MODEL)


def test_chat_logprobs():
    common.test_chat(TEST_MODEL, logprobs=True, top_logprobs=None)


def test_chat_top_logprobs():
    common.test_chat(TEST_MODEL, logprobs=True, top_logprobs=3)


if __name__ == "__main__":
    test_chat()
    test_chat_stream()
    test_chat_logprobs()
    test_chat_top_logprobs()
