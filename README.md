# AI Bricks

Simple, unified interface to multiple Generative AI providers and local model servers.

This project is similar in scope to [aisuite](https://github.com/andrewyng/aisuite), but with the following differences:

- stronger support for local model servers (tabbyAPI, KoboldCpp, LMStudio, Ollama, ...)
- more pythonic interface (nested dictionaries)
- configuration driven approach (yaml + jinja2)
- ability to record requests and responses (sqlite)
- minimal dependencies (requests, yamja)


## Example

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

