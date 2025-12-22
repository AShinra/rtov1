import streamlit as st
from db import get_collection, get_leave_types
from bson import ObjectId
from my_calendar import my_calendar, my_events
from datetime import datetime, time
from common import gradient_line
import pandas as pd


def user_info(fname: str):
    st.title("Leave Management")
    
    # get user collection data
    user_collection = get_collection('users')
    # get user document
    user_document = user_collection.find_one({'name': fname})

    # get related document ids
    role_id = user_document['role']
    info_id = user_document['user_info']
    leave_id = user_document['leave_credits']
    leave_data_id = user_document['leave_data']
    calendar_events_id = user_document['user_events']

    # get related documents
    role_collection = get_collection('user_role')
    role_document = role_collection.find_one({'_id': ObjectId(role_id)})

    info_collection = get_collection('users_info')
    info_document = info_collection.find_one({'_id': ObjectId(info_id)})

    leave_types_collection = get_leave_types()
    leave_types_documents = leave_types_collection.find()

    leave_credits_collection = get_collection('leave_credits')
    leave_credits_document = leave_credits_collection.find_one({'_id': ObjectId(leave_id)})

    leave_data_collection = get_collection('leave_data')
    leave_data_document = leave_data_collection.find_one({'_id': ObjectId(leave_data_id)})
    
    calendar_events_collection = get_collection('calendar_events')
    calendar_events_document = calendar_events_collection.find_one({'_id': ObjectId(calendar_events_id)})

    col1, col2 = st.columns([2, 3])
    with col1:
        gradient_line()
        with st.container():   
            st.markdown(f"## 👤{user_document['name']}")
            gradient_line()
            st.markdown(f"##### 🏬Department: {role_document['department']}")
            st.markdown(f"##### 💼Team: {role_document['team']}")
            # st.markdown(f"##### 🏠Address: {info_document['address']}")
            # st.markdown(f"##### 📱Mobile: {info_document['mobile_number']}")
            st.markdown(f"#####")
        
        cola, colb = st.columns([1, 2])
        with cola:

            leave_types = []

            for document in leave_types_documents:
                leave_types.append(document['name'])
            
            leave_types.sort()

            with st.container():
                st.markdown("### Leave Application")
                gradient_line()
                st.selectbox(
                    label="Select Leave Type",
                    options=leave_types,
                    key='leave_type_selectbox',
                    index=None,
                    placeholder='Select Leave Type',)
                st.date_input(
                    label="Select Leave Date",
                    key='leave_date_input',)
                st.text_area(
                    label="Reason for Leave",
                    key='leave_reason_textarea')
                st.button(
                    label="Submit Leave Application",
                    key='submit_leave_button',
                    use_container_width='stretch')
        with colb:
            st.markdown("### Leave Credits")
            gradient_line()
            colb1, colb2, colb3 = st.columns([2, 1, 1])
            with colb1:
                st.markdown("#### Current")
            with colb2:
                st.markdown("#### Used")
            with colb3:
                st.markdown("#### Balance")
            for leave_type in leave_types:

                try:
                    with colb1:
                        st.markdown(f'##### {leave_type}({leave_credits_document[leave_type]}):')
                    with colb2:
                        st.markdown(f'##### {len(leave_data_document[leave_type])}')
                    with colb3:
                        st.markdown(f"##### {leave_credits_document[leave_type]-len(leave_data_document[leave_type])}")
                except:
                    pass           
    with col2:

        tab1, tab2 = st.tabs(['📅**Calendar**', '🔖**Summary**'])

        with tab1:
            my_calendar(role_document['team'])
        with tab2:
            # get user role
            user_role = role_document['team'].split('-')[-1]

            logs = my_events(role_document['team'])
            
            # filter dataframe depending on role
            df = pd.DataFrame(logs)

            if df!=df.empty:

                # add new columns
                df[['Name', 'Leave Type']] = df['title'].str.split('-', expand=True)
                
                # remove other columns
                df.drop(columns=['title', 'backgroundColor'], inplace=True)

                # rename column
                df.rename(columns={'start': 'Date'}, inplace=True)

                # get unique list of user on the calendar
                users = set(df['Name'].to_list())    
            
                # sort alphabetically
                users = sorted(users)
                
                if user_role=='Member':
                    df = df[df['Name']==fname]
                    my_count = df.shape[0]
                    st.markdown(f'#### {fname} - logs ({my_count})')
                    df = df.reset_index(drop=True)
                    df.insert(0, "No.", df.index + 1)
                    col21, col22 = st.columns([4,1])
                    with col21:
                        st.dataframe(df, hide_index=True)
                    with col22:                
                        st.write(df['Leave Type'].value_counts())

                else:
                    # add user list to the selection box
                    select_name = st.selectbox(
                        label='Name',
                        options=users,
                        placeholder='Select Name',
                        index=None,
                        width=250)
                    
                    if select_name:
                        df = df[df['Name']==select_name]
                        my_count = df.shape[0]
                        st.markdown(f'#### {select_name} - logs ({my_count})')
                        df = df.reset_index(drop=True)
                        df.insert(0, "No.", df.index + 1)
                        col21, col22 = st.columns([4,1])
                        with col21:
                            st.dataframe(df, hide_index=True)
                        with col22:                
                            st.write(df['Leave Type'].value_counts())
                    else:
                        st.markdown(f'#### All - logs')
                        df = df.reset_index(drop=True)
                        df.insert(0, "No.", df.index + 1)
                        st.dataframe(df, hide_index=True)

            


        
    if st.session_state.get('submit_leave_button'):
        leave_type = st.session_state.leave_type_selectbox
        leave_input = datetime.combine(st.session_state.leave_date_input, time.min)
        leave_date = leave_input.strftime("%Y-%m-%d")
        leave_reason = st.session_state.leave_reason_textarea

        # get leave color
        document = leave_types_collection.find_one({'name': leave_type})
        leave_color = document['color']
        
        leave_data_collection.update_one(
            {"_id": ObjectId(leave_data_id)},
            {"$push": {leave_type: {
                'start': leave_date,
                'reason': leave_reason}}})
        calendar_events_collection.update_one(
            {"_id": ObjectId(calendar_events_id)},
            {"$push": {"events": {
                "title": f'{fname}-{leave_type}',
                "start": leave_date,
                "backgroundColor": leave_color
            }}})
        st.toast("Leave application submitted!")
        st.rerun()


    
    

    
