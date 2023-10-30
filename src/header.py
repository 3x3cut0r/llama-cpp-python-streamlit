import streamlit as st
from PIL import Image
favicon = Image.open('static/favicon.png')

# adds the teva logo to the sidebar
def logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebar"] {
                background-image: url(app/static/logo.png);
                background-repeat: no-repeat;
                background-position: 20px 20px;
                background-size: auto 80px;
            }
            
            [data-testid="stMarkdownContainer"] p {
                font-weight: bold;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

# call render method to set the header on every page
def render(page_title):
    # Page setup
    st.set_page_config(
        page_icon=favicon,
        page_title=page_title,
        layout='wide',
        initial_sidebar_state='expanded',
    )

    # Logo
    logo()
    
    st.title(page_title)
