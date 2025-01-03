from . import common

TEST_MODEL = "vllm:/opt/models/lm-studio/Qwen/Qwen2.5-Coder-3B-Instruct-GGUF/qwen2.5-coder-3b-instruct-q4_0.gguf"


def test_local_chat():
    common.test_chat(TEST_MODEL)


def test_local_chat_stream():
    common.test_chat_stream(TEST_MODEL)


if __name__ == "__main__":
    test_local_chat()
    test_local_chat_stream()