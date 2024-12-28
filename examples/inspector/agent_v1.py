import aibricks
from pathlib import Path


def chat_turn(user_input, client, config, chat_messages, full_chat_history, memory, n_messages):
    # get model response
    user_message = {'role': 'user', 'content': user_input}
    chat_messages += [user_message]
    full_chat_history += [user_message]
    
    response = client.chat(messages=chat_messages)
    content = response['choices'][0]['message']['content']
    assistant_message = {'role': 'assistant', 'content': content}
    chat_messages += [assistant_message]
    full_chat_history += [assistant_message]
    
    # process tools and collect responses
    responses = []
    for tag, attr, kw in aibricks.parse_xml(content):
        match attr['tool']:
            case 'respond':
                responses.append(kw['message'])
            case 'memory.add':
                memory += kw['new'] + '\n'
            case 'memory.replace':
                memory = memory.replace(kw['old'], kw['new'] or '')
    
    # update system prompt and trim history (only for chat_messages, not full_history)
    chat_messages[0]['content'] = config.render('system_prompt', memory=memory)
    full_chat_history[0]['content'] = chat_messages[0]['content']
    chat_messages[:] = chat_messages[0:1] + chat_messages[1:][-n_messages:]
    
    return responses, memory


def init_chat():
    config = aibricks.load_config(Path(__file__).with_name('agent_v1.yaml'))
    system_message = {'role': 'system', 'content': config.render('system_prompt', memory='')}
    return {
        'memory': '',
        'chat_messages': [system_message],
        'full_chat_history': [system_message],
        'config': config
    } 