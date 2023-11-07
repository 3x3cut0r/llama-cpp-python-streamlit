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