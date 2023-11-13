import requests
import json
import streamlit as st
import src.context as context
import urllib3

urllib3.disable_warnings()

# send request to API
def send(content_container):
    
    # create static json_data for all requests
    json_data = {
            "max_tokens": st.session_state['max_tokens'],
            "temperature": st.session_state['temperature'],
            "top_p": st.session_state['top_p'],
            "top_k": st.session_state['top_k'],
            "repeat_penalty": st.session_state['repeat_penalty'],
            "stop": st.session_state['stop'],
            "stream": st.session_state['stream']
        }
    
    # add endpoint specific json_data
    # endpoint = /v1/chat/completions
    if st.session_state['endpoint'] == "/v1/chat/completions":
      
        # add previous context to messages
        json_data['messages'] = context.get_history()
    
    # other endpoints
    else:
        json_data['prompt'] = context.get_history()
    
    # send json_data to endpoint
    try:
        s = requests.Session()
        headers = None
        with s.post(st.session_state["api_url"] + st.session_state['endpoint'],
            json=json_data,
            headers=headers,
            stream=st.session_state['stream'],
            timeout=240,
            verify=False
        ) as response:
          
            # if stream is True
            if st.session_state['stream']:
              
                # store chunks into context
                for chunk in response.iter_lines(chunk_size=None, decode_unicode=True):
                    
                    # fix error: Connection broken: InvalidChunkLength(got length b'', 0 bytes read)
                    if chunk == b'':   
                        continue
                    
                    # process chunk
                    elif chunk:
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
                            st.error(f'invalid JSON-String: {chunk}')

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
                    st.error(f'invalid JSON-String: {chunk}')

    except Exception as e:
        st.error(str(e))
        
# stop request
def stop(endpoint, stop):
    # send stop request to endpoint
    try:
        requests.post(
                st.session_state["api_url"] + endpoint,
                json={"messages": stop[0]},
                verify=False
            )
    except Exception as e:
        st.error(str(e))
