import json
import streamlit as st
from PIL import Image
favicon = Image.open('static/favicon.png')
import src.logo as logo
import src.styles as styles
import src.session as session
import src.sidebar as sidebar

# load title from config-file
with open("src/config.json", "r", encoding="utf-8") as file:
    config = json.load(file)

# call render method to set the header on every page
def render(page_title = None):
  
    # load page_title from config
    if page_title == None:
        if 'page_title' in config:
            page_title = config['page_title']
        else:
            page_title = "Model: Llama-2-7b-Chat"
  
    # page setup
    st.set_page_config(
        page_icon=favicon,
        page_title=page_title,
        layout='wide',
        initial_sidebar_state='expanded',
    )
    
    # render logo
    logo.render()
    
    # apply styles
    styles.render()
    
    # load config
    session.load()
    
    # render sidebar
    sidebar.render()

    # title
    st.title(page_title)
