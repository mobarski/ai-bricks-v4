# AI Bricks

AI Bricks provide minimalistic toolbox for creating Generative AI based systems.

Features:
- unified interface to multiple Generative AI providers
- strong support for local model servers (KoboldCpp, LMStudio, Ollama, LlamaCpp, tabbyAPI, ...)
- ability to record requests and responses (in sqlite) and generate reports (ie usage)
- configuration driven approach to prompt templates (yaml + jinja2)
- minimal dependencies (requests, yamja)

AI Bricks focuses on providing basic building blocks rather than a complex framework. This aligns with research showing that [the most successful LLM implementations use simple, composable patterns rather than complex frameworks](https://www.anthropic.com/research/building-effective-agents). By keeping things minimal, it allows developers to build exactly what they need without unnecessary abstractions.


## Example

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

# Supported providers

| Provider       | Example Connection String     | Environmental Variables  | Notes |
|----------------|-------------------------------|--------------------------|-------|
| **OpenAI**     | `openai:gpt-4o-mini`          | OPENAI_API_KEY           |       |
| **Google**     | `google:gemini-1.5-flash`     | GEMINI_API_KEY           |       |
| **OpenRouter** | `openrouter:openai/gpt-4o`    | OPENROUTER_API_KEY       |       |
| **ArliAI**     | `arliai:Llama-3.1-70B-Tulu-2` | ARLIAI_API_KEY           |       |
| **XAI**        | `xai:grok-beta`               | XAI_API_KEY              |       |
| **Together**   | `together:meta-llama/Meta-Llama-3-8B-Instruct-Turbo` | TOGETHER_API_KEY |  |
| **Ollama**     | `ollama:qwen2.5-coder:7b`     | -                        | GGUF  |
| **LMStudio**   | `lmstudio:qwen2.5-14b-instruct` | -                      | GGUF<br>dynamic model loading |
| **KoboldCpp**  | `koboldcpp`                   | -                        | GGUF  |
| **LlamaCpp**   | `llamacpp`                    | -                        | GGUF  |
| **tabbyAPI**   | `tabbyapi`                    | TABBYAPI_API_KEY         | EXL2, GPTQ |
| ~~dummy~~      | ~~`dummy`~~                   | -                        |       |
| ~~Anthropic~~  | ~~`anthropic:claude-3-5-sonnet`~~ | ANTHROPIC_API_KEY |       |


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
- [OpenAI Chat API](https://platform.openai.com/docs/api-reference/chat)
- [aisuite repo](https://github.com/andrewyng/aisuite)
- [ai-bricks-v3 repo](https://github.com/mobarski/ai-bricks-v3)
