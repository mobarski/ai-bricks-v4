import aibricks
from pathlib import Path

client = aibricks.client(model='xai:grok-beta')
config = aibricks.load_config(Path(__file__).parent / 'memgpt_v1.yaml')

messages = [{'role': 'system', 'content': config.render('system_prompt')}]


def chat_turn(user_input):
    global messages
    messages += [{'role': 'user', 'content': user_input}]
    response = client.chat(messages=messages)
    content = response['choices'][0]['message']['content']
    print(content)
    # TODO: parse xml
    # TODO: call tools
    # TODO: update prompt


if __name__ == '__main__':
    chat_turn("Hi! My name is Maciej and I'm from Poland!")
    chat_turn("I was born in 1981 and learned to program when I was 8.")
    chat_turn("Can you guess my first computer and programming language?")
