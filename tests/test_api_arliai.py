from . import common

TEST_MODEL = "arliai:Mistral-Nemo-12B-Instruct-2407"


def test_chat():
    common.test_chat(TEST_MODEL)


def test_chat_stream():
    # common.test_chat_stream(TEST_MODEL)
    raise Exception("Streaming is slow as hell for this model")


if __name__ == "__main__":
    test_chat()
    # test_chat_stream()
