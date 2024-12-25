# AI Bricks

AI Bricks provide minimalistic toolbox for creating Generative AI based systems.

Features:
- unified interface to multiple Generative AI providers
- strong support for local model servers (KoboldCpp, LMStudio, Ollama, LlamaCpp, tabbyAPI, ...)
- ability to record requests and responses (sqlite) and generate reports (ie usage)
- configuration driven approach (yaml + jinja2) to prompt templates
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
