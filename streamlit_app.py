import json
import requests
import streamlit as st
import src.header as header
import urllib3
urllib3.disable_warnings()

# Laden Sie die Konfigurationsdaten
with open("src/config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

# Header
header.render("Model: Llama-2-7b-Chat-GGUF")

context = ""

# Sidebar
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
          
# Send Request to API
def send_request():
    global context
  
    # endpoint = /v1/chat/completions
    json_data={
        "max_tokens": max_tokens,
        "temperature": temperature,
        "top_p": top_p,
        "top_k": top_k,
        "repeat_penalty": repeat_penalty,
        "stop": stop,
        "stream": stream,
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

    # send json_data to endpoint
    try:
        s = requests.Session()
        headers = None
        with s.post(
                config["api_url"] + "/v1/chat/completions",
                json=json_data,
                headers=headers,
                stream=stream,
                timeout=240,
                verify=False
            ) as response:
            response_title.markdown("Answer:\n")
            
            # if stream is True
            if stream:
                # store chunks into context
                for chunk in response.iter_lines(chunk_size=None, decode_unicode=True):
                    if chunk:
                        # skip [DONE] message
                        if chunk.startswith("data: [DONE]"):
                            continue
                        # remove "data: "-prefix, if present
                        elif chunk.startswith("data: "):
                            chunk = chunk[6:]
                        # skip ping messages
                        elif chunk.startswith(": ping"):
                            continue
                        
                        # add chunks content to the context
                        try:
                            chunk_dict = json.loads(chunk)
                            if 'choices' in chunk_dict:
                                if 'delta' in chunk_dict['choices'][0]:
                                    if 'content' in chunk_dict['choices'][0]['delta']:
                                        context = context + str(chunk_dict['choices'][0]['delta']['content'])
                                        response_placeholder.markdown(context)
                        except json.JSONDecodeError:
                            (f'Ungültiger JSON-String: {chunk}')

            # if stream is False
            else:
                # add complete content to the context
                try:
                    if response.ok:
                        context = response.json()['choices'][0]['message']['content']
                        response_placeholder.markdown(context)
                    else:
                        raise Exception(f'Error: {response.text}')
                except json.JSONDecodeError:
                    (f'Ungültiger JSON-String: {chunk}')

    except Exception as e:
        st.error(str(e))

# Stop Request
def stop_request():
    # send stop request to endpoint
    try:
        requests.post(
                config["api_url"] + "/v1/chat/completions",
                json={"messages": "STOPGENERATING"},
                verify=False
            )
    except Exception as e:
        st.error(str(e))

# GUI
response_title = st.empty()
response_placeholder = st.empty()

col1, col2 = st.columns(2)
with col1:
    user_content = st.text_input(label="Enter your message", value="", label_visibility="collapsed", placeholder="Enter your message")
with col2:
    generate_button = st.button('Generate', key='generate_button')

if generate_button:
    with st.spinner('Generating response...'):
        send_request()