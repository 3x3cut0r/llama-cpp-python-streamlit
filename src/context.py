from datetime import datetime
import streamlit as st
  
# render context in app
def render(container): # container = st.container()
    container.empty()
    
    with container.container():
        if st.session_state['context'] != []:
            for element in st.session_state['context']:
              
                # if question
                if 'question' in element:
                    q = element['question']
                    st.markdown(
                        f"""<p style="background-color: #343541; color: #ececf1; margin: 0px; padding: 20px;">{q}</p>""",
                        unsafe_allow_html=True,
                    )

                # if response   
                elif 'choices' in element and element['choices']:
                  
                    # if /v1/chat/completions endpoint
                    if 'message' in element['choices'][0]:
                        if 'content' in element['choices'][0]['message']:
                            c = element['choices'][0]['message']['content']
                            st.markdown(c)
                    
                    # if /v1/completions entpoint
                    elif 'text' in element['choices'][0]:
                        c = element['choices'][0]['text']
                        st.markdown(c)
    
# append user_content to context
def append_question(user_content): # user_content = question = string
    if st.session_state['context'] == [] or 'question' not in st.session_state['context'][-1] or st.session_state['context'][-1]['question'] != user_content:
        now = int(datetime.now().timestamp())
        st.session_state['context'].append({
            "id": 0, # todo: add question id here
            "question": user_content,
            "created": now
        })

# append context to context
def append(ctx): # ctx = python dict
    
    # rename ctx['choices'][0]['delta'] -> ctx['choices'][0]['message'] if ctx = chunk
    if 'choices' in ctx and ctx['choices']:
        if 'delta' in ctx['choices'][0]:
            ctx['choices'][0]['message'] = ctx['choices'][0].pop('delta')
    
    # check if 'id', 'created' and 'choices' exist
    if all(key in ctx for key in ('id', 'created', 'choices')):

        # check if ctx is already last element in context
        if st.session_state['context'] != [] and st.session_state['context'][-1]['id'] == ctx['id'] and st.session_state['context'][-1]['created'] == ctx['created']:
          
            # append chunk 'content' to existing (last) chunk 'content'
            if 'choices' in ctx and ctx['choices']:
              
                # for /v1/chat/completions endpoint
                if 'message' in ctx['choices'][0]:
                    if 'content' in ctx['choices'][0]['message']:
                        st.session_state['context'][-1]['choices'][0]['message']['content'] += ctx['choices'][0]['message'].get('content', '')
                
                # for /v1/completions entpoint
                elif 'text' in ctx['choices'][0]:
                    st.session_state['context'][-1]['choices'][0]['text'] += ctx['choices'][0].get('text', '')
        else:
          
            # append ctx to context
            if 'choices' in ctx and ctx['choices']:
              
                # for /v1/chat/completions endpoint
                if 'message' in ctx['choices'][0]:
                    if 'content' in ctx['choices'][0]['message']:
                        st.session_state['context'].append(ctx)
                
                # for /v1/completions entpoint        
                elif 'text' in ctx['choices'][0]:
                    st.session_state['context'].append(ctx)

    # raise error if no context was found
    else:
        raise Exception(f'Error: no context to append or wrong api endpoint\n\nmessage: {ctx}')

# return message from context
def get_message(ctx_element):
    
    # if question
    if 'question' in ctx_element:
        return "User: " + ctx_element['question'] + "\n"

    # if response   
    elif 'choices' in ctx_element and ctx_element['choices']:
      
        # if /v1/chat/completions endpoint
        if 'message' in ctx_element['choices'][0]:
            if 'content' in ctx_element['choices'][0]['message']:
                return "System: " + ctx_element['choices'][0]['message']['content'] + "\n"

        # if /v1/completions entpoint
        elif 'text' in ctx_element['choices'][0]:
            return "System: " + ctx_element['choices'][0]['text'] + "\n"

# return context history
def get_history():
    history = ""
    
    messages = [{
        "role": "system",
        "content": st.session_state['system_content']
    }]
    
    if st.session_state['context'] != []:
      
        # if context is enabled return all elements
        if st.session_state['enable_context']:
            for ctx_element in st.session_state['context']:
                history += get_message(ctx_element)

            # cut history to n_ctx length of llama.cpp server
            # todo: cut complete user and/or system message instead of cutting somewhere in the middle
            n_ctx = st.session_state['n_ctx']
            history = (history[-n_ctx:]) if len(history) >= n_ctx else history
                
        # if context is disabled return last element
        else:
            history += get_message(st.session_state['context'][-1])

    # message dict for /v1/chat/completions endpoint
    messages.append({
        "role": "user",
        "content": history
    })

    if st.session_state['endpoint'] == "/v1/chat/completions":
        return messages
    else:
        return st.session_state['prompt'].replace('{prompt}', history)
