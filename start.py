import streamlit as st
from argon2 import PasswordHasher
from db import get_collection
from common import gradient_line
from main import main


if __name__ == '__main__':

    st.markdown("""
        <style>
        h2, h3, h4, h5, h6 {
            margin-top: 0px !important;
            margin-bottom: 0px !important;
            padding-top: 0px !important;
            padding-bottom: 0px !important;
            line-height: 1.1;
        }
        </style>
        """, unsafe_allow_html=True)

    st.set_page_config(layout="wide")

    hide_streamlit_style = """<style>
    ._profileContainer_gzau3_63{display: none;}
    </style>"""
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    # hide streamlit toolbar
    st.markdown("""<style>[data-testid="stToolbar"] {display: none;}</style>""", unsafe_allow_html=True)
    st.markdown("""<style>[data-testid="manage-app-button"] {display: none !important;}</style>""", unsafe_allow_html=True)
    st.markdown("""<style>[data-testid="stSidebarCollapseButton"] {display: none !important;}</style>""", unsafe_allow_html=True)
    st.markdown("""<style>[data-testid="stSidebarHeader"] {height: 1rem;}</style>""", unsafe_allow_html=True)
    st.markdown("""<style>.stSidebar.st-emotion-cache-1legitb {background-color: black;}</style>""", unsafe_allow_html=True)
    
    # Global Title

    st.markdown(
    """
    <h2 style='text-align: center; 
               color: white; 
               background: linear-gradient(90deg, #35026eff 0%, #3a3b40 40%, #ffffff 100%);
               padding: 10px; 
               border-radius: 10px;'>
        📅 MMI Attendance Tracking System
    </h2>
    """,
    unsafe_allow_html=True)

    gradient_line()

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    if 'username' not in st.session_state:
        st.session_state.username = ''
    
    if 'rights' not in st.session_state:
        st.session_state.rights = ''
    
    if 'fname' not in st.session_state:
        st.session_state.fname = ''
    
    ph = PasswordHasher()
    user_collection = get_collection('users')    
        
    if st.session_state.logged_in:
        # main_start(st.session_state.fname, st.session_state.rights)
        main(st.session_state.fname, st.session_state.rights)
        with st.sidebar:
            if st.button('**Log Out**', use_container_width=True):
                st.session_state.logged_in = False
                st.rerun()           

    else:
        with st.sidebar:
            username = st.text_input(
                label="**USERNAME**",
                key='login_username')
            password = st.text_input(
                label="**PASSWORD**",
                type="password",
                key='login_password')
            submit_btn = st.button(
                label='**LOGIN**',
                use_container_width=True,
                key='login_submit_btn')            
            

        if submit_btn:
            doc = user_collection.find_one({"username": username})
            if not doc:
                st.sidebar.error("No such user")
            else:
                try:
                    ph.verify(doc["password_hash"], password)
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.rights = doc['rights']
                    st.session_state.fname = doc['name']
                    st.session_state.department = doc['department']
                    st.session_state.team = doc['team']
                except Exception:
                    st.sidebar.error("Wrong password")
                finally:    
                    st.rerun()
    
        
