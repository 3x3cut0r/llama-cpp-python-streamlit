import json
import streamlit as st

def render():
    with st.sidebar:
      
        # load endpoints from enpoints.json
        endpoints = []
        with open("src/endpoints.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            endpoints = list(data.keys())
        
        endpoint = st.selectbox("endpoint", endpoints)
        st.title("Model Settings")
        user_content = ""
        stream = st.toggle("stream results?", value=True)
        max_tokens = st.number_input("max_tokens", value=256, min_value=16, max_value=2048, step=1)
        temperature = st.number_input("temperature", value=0.2, min_value=0.01, max_value=1.99, step=0.05)
        top_p = st.number_input("top_p", value=0.95, min_value=0.0, max_value=1.0, step=0.05)
        top_k = st.number_input("top_k", value=40, min_value=1, max_value=200, step=1)
        repeat_penalty = st.number_input("repeat_penalty", value=1.1, min_value=1.0, max_value=1.5, step=0.05)
        stop =  st.text_input("stop", value=r'\n, ###')
        stop = stop.encode().decode('unicode_escape')
        stop = stop.replace(" ", "").split(",")
        if endpoint == "/v1/chat/completions":
            system_content = st.text_area("system_content", value="You are a helpful assistant.", height=200)
        else:
            system_content = st.text_area("system_content", value=r"\n\n### Instructions:\n{prompt}\n\n### Response:\n", height=200)
            system_content = system_content.encode().decode('unicode_escape')
            st.markdown("hint: the expression `{prompt}` must exist!", unsafe_allow_html=True)
        
        return endpoint, user_content, stream, max_tokens, temperature, top_p, top_k, repeat_penalty, stop, system_content 
