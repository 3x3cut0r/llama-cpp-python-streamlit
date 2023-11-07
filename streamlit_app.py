import streamlit as st
import src.header as header
import src.sidebar as sidebar
import src.request as request
import src.context as context

# render header
header.render()

# render sidebar
(endpoint, user_content, stream, max_tokens, temperature, top_p, top_k, repeat_penalty, stop, system_content) = sidebar.render()        

# initialize context in session state if not present
if 'context' not in st.session_state:
    st.session_state['context'] = []

# render content_container
content_container = st.empty()

# render context
if 'context' in st.session_state:
    context.render(content_container)

# render message-text_input + generate-submit_button
with st.form("Prompt Form", clear_on_submit=True):
    col1, col2 = st.columns([2,1])
    
    with col1:
        user_content = st.text_input(label="Enter your message", value="", label_visibility="collapsed", placeholder="Enter your message")
    
    with col2:
        generate_button = st.form_submit_button('Generate')

    if generate_button:
        context.append_question(user_content)
        context.render(content_container)
        
        with st.spinner('Generating response...'):
            request.send(endpoint, user_content, stream, max_tokens, temperature, top_p, top_k, repeat_penalty, stop, system_content, content_container)