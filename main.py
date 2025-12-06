import streamlit as st
from streamlit_option_menu import option_menu
from common import gradient_line
from attendance import user_info




def main(fname: str, rights: str, department: str, team: str):

    with st.sidebar:
        st.markdown(
            f"""
            <h2 style='text-align: left; color: #ffff; margin: 0; line-height: 1; padding: 0;'>
            {fname}👤
            </h2>
            <h3 style='text-align: left; color: #ffff; margin: 0; line-height: 1; padding: 0;'>
            Department: {department} - {team}
            </h3>
            """,
            unsafe_allow_html=True)
        
        gradient_line()

        selected_option = option_menu(
            menu_title=None,
            options=['Home', 'Leave', 'Reports'],
            icons=['house', 'check-square', 'bar-chart'],
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
    
    if selected_option == 'Leave':
        st.title('Leave Management')
        user_info(fname)
    
    
