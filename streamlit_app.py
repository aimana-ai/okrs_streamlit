import streamlit as st
import pickle
import streamlit_authenticator as stauth
import yaml
from streamlit_option_menu import option_menu

st.set_page_config(page_title="Chat", page_icon=None, layout="centered", initial_sidebar_state="collapsed", menu_items=None)
## REMOVE STREAMLIT HEADER AND FOOTER
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


    
    # --- PAGE SETUP ---
about_page = st.Page(
    page = "views/about.py",
    title = "Sobre",
    icon = ":material/account_circle:", #https://fonts.google.com/icons
   
    )

chatbot_page = st.Page(
    page = "views/chatbot.py",
    title = "Chat",
    icon = ":material/chat:" ,
    default = True
    )

settings_page = st.Page(
    page = "views/settings.py",
    title = "Settings",
    icon = ":material/settings:" 
    )

knowledge_base_page = st.Page(
    page = "views/knowledge_base.py",
    title = "Knowledge Base",
    icon = ":material/auto_stories:"
    )



    # --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
pg = st.navigation(pages = [about_page, chatbot_page])#, knowledge_base_page, settings_page])

    # --- SHARED ON ALL PAGES ---
st.logo("assets/logo.jpeg")
st.sidebar.markdown("""
        <style>
        [data-testid='stSidebarNav'] > ul {
            min-height: 70vh;
        } 
        </style>
        """, unsafe_allow_html=True)
st.sidebar.text("Developed by AImana")
st.sidebar.text("Version 0.0.1")

# --- RUN NAVIGATION ---
pg.run()

