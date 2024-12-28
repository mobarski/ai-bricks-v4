# REF: https://docs.streamlit.io/develop/api-reference/chat

import streamlit as st
import aibricks
from pathlib import Path
import agent_v1


MODELS = [
    'xai:grok-beta',
    'openai:gpt-4o',
    'openai:gpt-4o-mini',
    'deepseek:deepseek-chat',
    'google:gemini-2.0-flash-exp',
    'google:gemini-1.5-flash',
    'google:gemini-1.5-flash-8b',
    'openrouter:nousresearch/hermes-3-llama-3.1-70b'
]


# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if 'memory' not in st.session_state:
    chat_state = agent_v1.init_chat()
    st.session_state.memory = chat_state['memory']
    st.session_state.chat_messages = chat_state['chat_messages']
    st.session_state.full_chat_history = chat_state['full_chat_history']
    st.session_state.agent_config = chat_state['config']
    st.session_state.n_messages = 4


def update_chat_messages(new_n_messages):
    if new_n_messages > len(st.session_state.chat_messages) - 1:  # -1 for system message
        history_messages = st.session_state.full_chat_history[1:]  # Skip system message
        st.session_state.chat_messages = (
            st.session_state.chat_messages[0:1] +  # Keep system message
            history_messages[-new_n_messages:]  # Get up to new_n_messages from full history
        )
    else:
        st.session_state.chat_messages = (
            st.session_state.chat_messages[0:1] + 
            st.session_state.chat_messages[1:][-new_n_messages:]
        )


# Sidebar
with st.sidebar:
    model = st.selectbox("Model", MODELS)
    new_n_messages = st.slider("Number of messages to send", 2, 30, st.session_state.n_messages, 2)
    
    if new_n_messages != st.session_state.n_messages:
        st.session_state.n_messages = new_n_messages
        update_chat_messages(new_n_messages)
        st.rerun()
    
    with st.expander("Messages"):
        st.write(st.session_state.chat_messages[1:])
    with st.expander("Memory"):
        st.write(st.session_state.memory)


# Initialize client
client = aibricks.client(model=model)


# Chat interface
st.markdown("### Chat")


def render_message(message):
    if message["role"] == "user":
        with st.chat_message("user"):
            st.markdown(message["content"])
        return

    raw_message = next(
        msg["content"] 
        for msg in st.session_state.full_chat_history 
        if msg["role"] == "assistant" and msg["content"].find(message["content"]) != -1
    )
    
    for tag, attr, kw in aibricks.parse_xml(raw_message):
        with st.chat_message("assistant"):
            match attr['tool']:
                case 'respond':
                    st.markdown(kw['message'])
                case 'memory.add':
                    st.markdown("<span style='color: #A0A0A0'>🧠 *Adding to memory:* " + kw['new'] + "</span>", unsafe_allow_html=True)
                case 'memory.replace':
                    st.markdown(f"<span style='color: #A0A0A0'>🔄 *Updating memory:* replacing '{kw['old']}' with '{kw['new']}'</span>", unsafe_allow_html=True)


# Display messages
for message in st.session_state.messages:
    render_message(message)


# Handle user input
if prompt := st.chat_input("What is up?"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    responses, st.session_state.memory = agent_v1.chat_turn(
        prompt, 
        client, 
        st.session_state.agent_config,
        st.session_state.chat_messages,
        st.session_state.full_chat_history,
        st.session_state.memory,
        st.session_state.n_messages
    )
    
    for response in responses:
        st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
