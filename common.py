import streamlit as st

def gradient_line():
    st.markdown("<hr style='border: 0; height: 10px; padding: 0; margin: 0; background: linear-gradient(to right, #444, #bbb);'/>", unsafe_allow_html=True)

def get_logo():
    # Return a path or bytes object for the logo image if you have one.
    return None

def get_user_document_ids(document):
    # Extract and return user document IDs from the given document.
    role_id = document['role']
    info_id = document['user_info']
    leave_id = document['leave_credits']
    leave_data_id = document['leave_data']
    leave_credits_id = document['leave_credits']
    calendar_events_id = document['user_events']

    return [role_id, info_id, leave_id, leave_data_id, leave_credits_id, calendar_events_id]    