from . import common

TEST_MODEL = "gpt4all:Reasoner v1"


def test_local_chat():
    common.test_chat(TEST_MODEL)


def test_local_chat_stream():
    # common.test_chat_stream(TEST_MODEL)
    raise Exception("Streaming doesn't work")


if __name__ == "__main__":
    test_local_chat()
    # test_local_chat_stream()
