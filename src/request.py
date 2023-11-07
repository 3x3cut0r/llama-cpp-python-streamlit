import requests
import json
import streamlit as st
import src.context as context
import urllib3

urllib3.disable_warnings()

# load config-file
with open("src/config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

# send request to API
def send(endpoint, user_content, stream, max_tokens, temperature, top_p, top_k, repeat_penalty, stop, system_content, content_container):
    json_data = {
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "repeat_penalty": repeat_penalty,
            "stop": stop,
            "stream": stream
        }
    
    # endpoint = /v1/chat/completions
    if endpoint == "/v1/chat/completions":
        json_data['messages'] = [
                {
                    "content": system_content,
                    "role": "system"
                },
                {
                    "content": user_content,
                    "role": "user"
                }
            ]
    
    # other endpoints
    else:
        system_content = system_content.replace('{prompt}', user_content)
        json_data['prompt'] = system_content

    # send json_data to endpoint
    try:
        s = requests.Session()
        headers = None
        with s.post(config["api_url"] + endpoint,
            json=json_data,
            headers=headers,
            stream=stream,
            timeout=240,
            verify=False
        ) as response:
          
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
                        
                        # append chunks content to the context
                        try:
                            chunk_dict = json.loads(chunk)
                            context.append(chunk_dict)
                            context.render(content_container)
                        except json.JSONDecodeError:
                            (f'invalid JSON-String: {chunk}')

            # if stream is False
            else:
                # append complete content to the context
                try:
                    if response.ok:
                        context.append(response.json())
                        context.render(content_container)
                    else:
                        raise Exception(f'Error: {response.text}')
                except json.JSONDecodeError:
                    (f'invalid JSON-String: {chunk}')

    except Exception as e:
        st.error(str(e))
        
# stop request
def stop(endpoint, stop):
    # send stop request to endpoint
    try:
        requests.post(
                config["api_url"] + endpoint,
                json={"messages": stop[0]},
                verify=False
            )
    except Exception as e:
        st.error(str(e))