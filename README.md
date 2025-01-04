# AI Bricks

AI Bricks provide minimalistic toolbox for creating Generative AI based systems.

Features:
- unified interface to multiple Generative AI providers
- strong support for local model servers (KoboldCpp, LMStudio, Ollama, LlamaCpp, tabbyAPI, ...)
- ability to record requests and responses (in sqlite) and generate reports (ie usage)
- configuration driven approach to prompt templates (yaml + jinja2)
- minimal dependencies (requests, yamja)

AI Bricks focuses on providing basic building blocks rather than a complex framework. This aligns with research showing that [the most successful LLM implementations use simple, composable patterns rather than complex frameworks](https://www.anthropic.com/research/building-effective-agents). By keeping things minimal, it allows developers to build exactly what they need without unnecessary abstractions.


## Examples

Example from the [aisuite](https://github.com/andrewyng/aisuite) repo:
```python
import aibricks
client = aibricks.client()

models = ["openai:gpt-4o", "xai:grok-beta"]

messages = [
    {"role": "system", "content": "Respond in Pirate English."},
    {"role": "user", "content": "Tell me a joke."},
]

for model in models:
    response = client.chat(
        model=model,
        messages=messages,
        temperature=0.75
    )
    print(response['choices'][0]['message']['content'])
```

#### Common Vision API

```python
import aibricks
client = aibricks.client()

models = ["openai:gpt-4o", "xai:grok-vision-beta", 'anthropic:claude-3-5-sonnet-latest']

messages = [
    {"role": "user", "content": [
        {"type": "text", "text": "what these two images have in common?"},
        {"type": "image_url", "image_url": {"url": "https://example.com/image1.jpg"}},
        {"type": "image_url", "image_url": {"url": "file://path/to/image2.jpg", "detail": "high"}},
    ]},
]

for model in models:
    response = client.chat(
        model=model,
        messages=messages,
    )
    print(response)
```

#### Minimalistic implementation of MemGPT-like agent
This example can be found in the [examples/memgpt](examples/memgpt) directory.


# Supported providers

| Provider       | Example Connection String           | Environmental Variables  | Notes  |
|----------------|-------------------------------------|--------------------------|--------|
| **OpenAI**     | `openai:gpt-4o-mini`                | OPENAI_API_KEY           |        |
| **Anthropic**  | `anthropic:claude-3-5-haiku-latest` | ANTHROPIC_API_KEY        |        |
| **XAI**        | `xai:grok-beta`                     | XAI_API_KEY              |        |
| **Google**     | `google:gemini-1.5-flash`           | GEMINI_API_KEY           |        |
| **DeepSeek**   | `deepseek:deepseek-chat`            | DEEPSEEK_API_KEY         |        |
| **OpenRouter** | `openrouter:openai/gpt-4o`          | OPENROUTER_API_KEY       |        |
| **ArliAI**     | `arliai:Llama-3.1-70B-Tulu-2`       | ARLIAI_API_KEY           |        |
| **Together**   | `together:google/gemma-2b-it`       | TOGETHER_API_KEY         | 🚧🚧🚧 |
| **HuggingFace**| `huggingface:meta-llama/Meta-Llama-3-8B-Instruct-Turbo` | HUGGINGFACE_API_KEY | 🚧🚧🚧 |
| **Ollama**     | `ollama:qwen2.5-coder:7b`           | -                        | GGUF   |
| **LMStudio**   | `lmstudio:qwen2.5-14b-instruct`     | -                        | GGUF<br>dynamic model loading |
| **KoboldCpp**  | `koboldcpp`                         | -                        | GGUF   |
| **LlamaCpp**   | `llamacpp`                          | -                        | GGUF   |
| **tabbyAPI**   | `tabbyapi`                          | TABBYAPI_API_KEY         | EXL2, GPTQ |
| **GPT4All**    | `gpt4all:Reasoner v1`               | -                        | GGUF<br>buggy |
| **vLLM**       | `vllm:/opt/models/qwen2.5-coder-3b-instruct-q4_0.gguf` | - | GGUF |
| **dummy**      | `dummy`                             | -                        |        |


# License

MIT

# Installation

Don't. The project is still in its infancy.


# References

- [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
- [Building an AI-Powered Game](https://learn.deeplearning.ai/courses/building-an-ai-powered-game)
- [LLMs as Operating Systems: Agent Memory](https://learn.deeplearning.ai/courses/llms-as-operating-systems-agent-memory)
- [Letta (formerly MemGPT)](https://github.com/letta-ai/letta)
- [MemGPT: Towards LLMs as Operating Systems](https://arxiv.org/abs/2310.08560)
- [Cognitive load is what matters](https://minds.md/zakirullin/cognitive)
- [aisuite repo](https://github.com/andrewyng/aisuite)
- [ai-bricks-v3 repo](https://github.com/mobarski/ai-bricks-v3)

#### Chat API docs
- [OpenAI Chat API](https://platform.openai.com/docs/api-reference/chat)
- [Anthropic Messages API](https://docs.anthropic.com/en/api/messages)
- [XAI Chat Completion](https://docs.x.ai/docs/api-reference#chat-completions)
- [Google Text Generation](https://ai.google.dev/gemini-api/docs/text-generation)
- [DeepSeek Docs](https://api-docs.deepseek.com/)
- [OpenRouter Quick Start](https://openrouter.ai/docs/quick-start)
- [ArliAI Usage Docs](https://www.arliai.com/docs)
- [Together Chat API](https://docs.together.ai/docs/chat-overview)
- [HuggingFace API](https://huggingface.co/docs/api-inference/index)

#### Vision API docs
- [OpenAI Vision API](https://platform.openai.com/docs/guides/vision)
- [Anthropic Vision API](https://docs.anthropic.com/en/docs/build-with-claude/vision)

#### Local model servers
- [Ollama](https://ollama.ai/)
- [LMStudio](https://lmstudio.ai/)
- [KoboldCpp](https://github.com/LostRuins/koboldcpp)
- [LlamaCpp](https://github.com/ggerganov/llama.cpp)
- [tabbyAPI](https://github.com/theroyallab/tabbyAPI)
- [GPT4All](https://gpt4all.io/index.html?ref=localhost)
- [vLLM](https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html)

#### Local model servers (TODO)
- [LocalAI](https://github.com/mudler/LocalAI)
- [Fast-LLM](https://github.com/ServiceNow/Fast-LLM)
- [TGI](https://huggingface.co/docs/text-generation-inference/en/index)
