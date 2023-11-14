import streamlit as st

 # render logo
def render():
    st.markdown(
        f"""
        <style>          
            [data-testid="stSidebar"] {{
                background-image: url(app/static/logo.png);
                background-repeat: no-repeat;
                background-position: 20px 20px;
                background-size: auto 80px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
