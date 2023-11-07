import json
import streamlit as st

def render():
    with st.sidebar:
      
        # load endpoints from enpoints.json
        endpoints = []
        with open("src/endpoints.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            endpoints = list(data.keys())
        
        # endpoint
        endpoint = st.selectbox("endpoint", endpoints)
        st.session_state['endpoint'] = endpoint
        
        # sidebar_title
        st.title("Model Settings")
        st.session_state['sidebar_title'] = "Model Settings"
        
        # user_content
        user_content = ""
        st.session_state['user_content'] = user_content
        
         # enable_context
        enable_context = st.toggle("enable context?", value=True) if endpoint == "/v1/chat/completions" else False
        st.session_state['enable_context'] = enable_context
        
        # stream
        stream = st.toggle("stream results?", value=True)
        st.session_state['stream'] = stream
        
        # max_tokens
        max_tokens = st.number_input("max_tokens", value=256, min_value=16, max_value=2048, step=1)
        st.session_state['max_tokens'] = max_tokens
        
        # temperature
        temperature = st.number_input("temperature", value=0.2, min_value=0.01, max_value=1.99, step=0.05)
        st.session_state['temperature'] = temperature
        
        # top_p
        top_p = st.number_input("top_p", value=0.95, min_value=0.0, max_value=1.0, step=0.05)
        st.session_state['top_p'] = top_p
        
        # top_k
        top_k = st.number_input("top_k", value=40, min_value=1, max_value=200, step=1)
        st.session_state['top_k'] = top_k
        
        # repeat_penalty
        repeat_penalty = st.number_input("repeat_penalty", value=1.1, min_value=1.0, max_value=1.5, step=0.05)
        st.session_state['repeat_penalty'] = repeat_penalty
        
        # stop
        stop =  st.text_input("stop", value=r'\n, ###')
        stop = stop.encode().decode('unicode_escape')
        stop = stop.replace(" ", "").split(",")
        st.session_state['stop'] = stop
        
        if endpoint == "/v1/chat/completions":
            system_content = st.text_area("system_content", value="A dialog, where User interacts with AI. AI is helpful, kind, obedient, honest, and knows its own limits.", height=200)
        else:
            system_content = st.text_area("system_content", value=r"\n\n### Instructions:\n{prompt}\n\n### Response:\n", height=200)
            system_content = system_content.encode().decode('unicode_escape')
            st.markdown("hint: the expression `{prompt}` must exist!", unsafe_allow_html=True)
        st.session_state['system_content'] = system_content
