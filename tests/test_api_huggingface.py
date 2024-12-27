from . import common

TEST_MODEL = "huggingface:meta-llama/Meta-Llama-3-8B-Instruct-Turbo"


def test_chat():
    common.test_chat(TEST_MODEL)


def test_chat_stream():
    common.test_chat_stream(TEST_MODEL)


if __name__ == "__main__":
    test_chat()
    test_chat_stream()

# TODO: FIX ERRORS
