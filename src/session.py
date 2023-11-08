import json
import streamlit as st

# load config-file
def load():
    # initialize context in session state if not present
    if 'context' not in st.session_state:
        st.session_state['context'] = []
    
    # load config in session state
    with open("src/config.json", "r", encoding="utf-8") as file:
        config = json.load(file)
        st.session_state['api_url'] = config['api_url'] if 'api_url' in config else "http://localhost:8000"
        st.session_state['title'] = config['title'] if 'title' in config else "Llama-2-7b-Chat"
        st.session_state['n_ctx'] = int(config['n_ctx']) if 'n_ctx' in config else 2048
        st.session_state['enable_context'] = config['enable_context'] if 'enable_context' in config else True
        st.session_state['stream'] = config['stream'] if 'stream' in config else True
        st.session_state['max_tokens'] = int(config['max_tokens']) if 'max_tokens' in config else 256
        st.session_state['temperature'] = float(config['temperature']) if 'temperature' in config else 0.2
        st.session_state['top_p'] = float(config['top_p']) if 'top_p' in config else 0.95
        st.session_state['top_k'] = int(config['top_k']) if 'top_k' in config else 40
        st.session_state['repeat_penalty'] = float(config['repeat_penalty']) if 'repeat_penalty' in config else 1.1
        st.session_state['stop'] = config['stop'] if 'stop' in config else "###"
        st.session_state['system_content'] = config['system_content'] if 'system_content' in config else "User asks Questions to the AI. AI is helpful, kind, obedient, honest, and knows its own limits."
        st.session_state['prompt'] = config['prompt'] if 'prompt' in config else "### Instructions:\n{prompt}\n\n### Response:\n"
