import json
import requests
import streamlit as st
import src.header as header

api_url = 'https://llama-cpp-python.3x3cut0r.de'
api_endpoint = '/v1/chat/completions'
answer = ""

header.render("Model: Llama-2-7b-Chat-GGUF")

def send_request():
    json_data={
        "max_tokens": max_tokens,
        "messages": [
            {
                "content": system_content,
                "role": "system"
            },
            {
                "content": user_content,
                "role": "user"
            }
        ]
    }
    headers = {'Content-Type': 'application/json', 'Accept-Charset': 'UTF-8'}
    response = requests.post(api_url + api_endpoint,
                             json=json_data,
                             headers=headers,
                             timeout=240,
                             verify=False
                             )
    if response.ok:
        return response.json()
    else:
        raise Exception(f'Error: {response.text}')

with st.sidebar:
    st.title("Model Settings")
    user_content = ""
    stream = st.toggle("stream results?", value=True)
    max_tokens = st.number_input("max_tokens", value=256, min_value=32, max_value=2048, step=1)
    temperature = st.number_input("temperature", value=0.2, min_value=0.0, max_value=1.0, step=0.05)
    top_p = st.number_input("top_p", value=0.95, min_value=0.0, max_value=1.0, step=0.05)
    top_k = st.number_input("top_k", value=40, min_value=1, max_value=1024, step=1)
    repeat_penalty = st.number_input("repeat_penalty", value=1.1, min_value=1.1, max_value=2.0, step=0.05)
    system_content = st.text_area("system_content", value="You are a helpful assistant.")
    stop = ["STOPGENERATING"]

col1, col2 = st.columns(2)
with col1:
    user_content = st.text_input(label="Enter your message", value="", label_visibility="collapsed", placeholder="Enter your message")
with col2:
    generate_button = st.button('Generate')

if generate_button:
    with st.spinner('Generating response...'):
        try:
            response = send_request()
            answer = response['choices'][0]['message']['content']
        except Exception as e:
            st.error(str(e))

st.markdown(answer)