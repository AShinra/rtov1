import streamlit as st
from streamlit_option_menu import option_menu
from common import gradient_line
from attendance import user_info
from admin_tools import user_management
from my_clocks import flip_clock, digital_clock
from bible_verses import get_random_bible_verse




def main(fname: str, rights: str):

    if rights == 'admin':
        menu_title = 'Admin Dashboard'
        menu_options = ['Home', 'User Management', 'Leave Management', 'Reports']
        icons = ['house', 'people-fill', 'check-square', 'bar-chart']
    else:
        menu_title = 'User Dashboard'
        menu_options = ['Home', 'Leave Management', 'Reports']
        icons = ['house', 'check-square', 'bar-chart']

    with st.sidebar:

        digital_clock()

        st.markdown('# Word of GOD')
        st.markdown(f'### {get_random_bible_verse()}')
        st.markdown('##    ')

        st.markdown(
            f"""
            <h2 style='text-align: left; color: #ffff; margin: 0; line-height: 1; padding: 0;'>
            {fname}👤
            </h2>
            """,
            unsafe_allow_html=True)
        
        gradient_line()

        selected_option = option_menu(
            menu_title=menu_title,
            options=menu_options,
            icons=icons,
            menu_icon="cast",
            default_index=0,
            orientation="vertical",
            styles={
                "icon": {"color": "#ffff"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#444"},
                "nav-link-selected": {"background-color": "#444"},
            })
        
    
        st.button(label='Reset', key='reset_button', use_container_width=True)
        if st.session_state.reset_button:
            st.rerun()
    
        
    
    if selected_option == 'Leave Management':
        user_info(fname)
    
    elif selected_option == 'User Management':
        user_management()
    
    
