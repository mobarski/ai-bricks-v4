import aibricks
from pathlib import Path

client = aibricks.client(model='xai:grok-beta')
config = aibricks.load_config(Path(__file__).parent / 'memgpt_v1.yaml')

memory = ''
messages = [{'role': 'system', 'content': config.render('system_prompt', memory=memory)}]
N_MESSAGES_TO_KEEP = 4


def chat_turn(user_input):
    global messages, memory
    # get model response
    messages += [{'role': 'user', 'content': user_input}]
    response = client.chat(messages=messages)
    content = response['choices'][0]['message']['content']
    messages += [{'role': 'assistant', 'content': content}]
    # handle tool usage
    for tag, attr, kw in aibricks.parse_xml(content):
        tool = attr['tool']
        if tool == 'respond':
            print('AI:', kw['message'])
        elif tool == 'memory.add':
            memory += kw['new'] + '\n'
        elif tool == 'memory.replace':
            memory = memory.replace(kw['old'], kw['new'])
    # update system prompt with new memory
    messages[0]['content'] = config.render('system_prompt', memory=memory)
    # evict old messages
    messages = messages[0:1] + messages[1:][-N_MESSAGES_TO_KEEP:]


if __name__ == '__main__':
    chat_turn("Hi! My name is Maciej and I'm from Poland!")
    chat_turn("I was born in 1981 and learned to program when I was 8.")
    chat_turn("Can you guess my first computer and programming language?")
    chat_turn("Well, it was Timex 2048 and BASIC.")
    print('\nMEMORY:\n' + memory)
