import streamlit as st

 # render styles
def render():
    st.markdown(
        f"""
        <style>          
            [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
                padding-top: 20px;
            }}
            
            [data-testid="stForm"] {{
                border: none;
                padding-left: 0px;
            }}
            
            [data-testid="stMarkdownContainer"] {{
                font-weight: normal;
            }}
            
            [data-testid="stMarkdown"] p,
            [data-testid="stMarkdown"] ol {{
                background-color: #444654;
                color: #ced2d8;
                margin: 0px;
                padding: 20px;
            }}
            
            [data-testid="stMarkdown"] [data-testid="stCodeBlock"] {{
                background-color: #444654;
                color: #ced2d8;
                margin: 0px;
                padding-left: 10px;
                padding-right: 10px;
            }}
            
            [data-testid="stCodeBlock"] {{
                margin: 0px;
                padding-left: 10px;
            }}
            
            .st-es {{
                min-height: 55px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )
