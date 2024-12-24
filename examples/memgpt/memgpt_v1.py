import aibricks
from pathlib import Path

client = aibricks.client(model='xai:grok-beta')
config = aibricks.load_config(Path(__file__).parent / 'memgpt_v1.yaml')

messages = [
    {'role': 'system', 'content': config.render('system_prompt')},
]


def main_loop():
    response = client.chat(messages=messages)
    content = response['choices'][0]['message']['content']
    print(content)
    # TODO: parse xml
    # TODO: call tools
    # TODO: update prompt


if __name__ == '__main__':
    messages += [{'role': 'user', 'content': "Hi! My name is Maciej and I'm from Poland!!"}]
    main_loop()
