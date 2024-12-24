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
        temperature=0.25
    )
    print(response['choices'][0]['message']['content'])
