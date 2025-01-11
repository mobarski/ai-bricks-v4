from . import common

TEST_MODEL = "lmstudio"


def test_local_chat():
    common.test_chat(TEST_MODEL)


def test_local_chat_stream():
    common.test_chat_stream(TEST_MODEL)


def test_local_chat_logprobs():
    common.test_chat(TEST_MODEL, logprobs=True, top_logprobs=None)  # ERROR: ignored


def test_local_chat_top_logprobs():
    common.test_chat(TEST_MODEL, logprobs=True, top_logprobs=3)  # ERROR: ignored


if __name__ == "__main__":
    test_local_chat()
    test_local_chat_stream()
    test_local_chat_logprobs()
    test_local_chat_top_logprobs()
