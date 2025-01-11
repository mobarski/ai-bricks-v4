from . import common

TEST_MODEL = "arliai:Mistral-Nemo-12B-Instruct-2407"


def test_chat():
    common.test_chat(TEST_MODEL)


def test_chat_stream():
    # common.test_chat_stream(TEST_MODEL)
    raise Exception("Streaming is slow as hell for this model")


def test_chat_logprobs():
    common.test_chat(TEST_MODEL, logprobs=True, top_logprobs=None)


def test_chat_top_logprobs():
    # common.test_chat(TEST_MODEL, logprobs=True, top_logprobs=3)
    raise Exception("Streaming is slow as hell for this model")


if __name__ == "__main__":
    test_chat()
    # test_chat_stream()
    test_chat_logprobs()
    # test_chat_top_logprobs()
