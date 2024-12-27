from . import common

TEST_MODEL = "dummy:xxx"


def test_local_chat():
    common.test_chat(TEST_MODEL)


def test_local_chat_stream():
    common.test_chat_stream(TEST_MODEL)


if __name__ == "__main__":
    test_local_chat()
    test_local_chat_stream()

# TODO: FIX ERRORS
