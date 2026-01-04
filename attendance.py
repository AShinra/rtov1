import streamlit as st
from db import get_collection, get_leave_types
from bson import ObjectId
from my_calendar import my_calendar, my_events
from datetime import datetime, time, date
from common import gradient_line, get_user_document_ids
import pandas as pd



def user_info(fname: str, rights: str):
    st.title("Leave Management")
    
    # get user collection data
    user_collection = get_collection('users')
    # get user document
    user_document = user_collection.find_one({'name': fname})

    # get team and team_role
    team = user_document['team']
    team_role = user_document['team_role']
    department = user_document['department']
    address = user_document['address']
    mobile_number = user_document['mobile_number']

    birthdate_str = user_document['birthdate']
    date_obj = datetime.strptime(birthdate_str, "%Y-%m-%d")
    birthdate = date_obj.strftime("%B %d, %Y")

    # get related document ids
    leave_id = user_document['leave_credits']

    # get related documents
    user_leave_data_collection = get_collection('user_leave_data')

    leave_types_collection = get_leave_types()
    leave_types_documents = leave_types_collection.find()

    leave_credits_collection = get_collection('leave_credits')
    leave_credits_document = leave_credits_collection.find_one({'_id': ObjectId(leave_id)})

    col1, col2 = st.columns([4, 6], border=True)
    with col1:
        gradient_line()
        st.markdown(f"## 👤{user_document['name']}")
        gradient_line()
        st.markdown(f"##### 🏬Department: {department}")
        st.markdown(f"##### 💼Team: {team}")
        st.markdown(f"##### 🛠️Role: {team_role}")
        with st.expander(label="👤 User Information"):   
            st.markdown(f"##### 🏠Address: {address}")
            st.markdown(f"##### 📱Mobile: {mobile_number}")
            st.markdown(f"##### 📅Birthdate: {birthdate}")

        leave_types = []
        
        for data in leave_credits_document:
            if data!='_id':
                if leave_credits_document[data]>0:
                    leave_types.append(data)
        
        leave_types.sort()

        with st.expander(label="ℹ️ Leave Credits Information"):
            colb1, colb2, colb3 = st.columns([4, 3, 4])
            with colb1:
                st.markdown("##### Type")
            with colb2:
                st.markdown("##### Used")
            with colb3:
                st.markdown("##### Available")

            current_year = date.today().year
                    
            for leave_type in leave_types:

                try:
                    with colb1:
                        st.markdown(f'###### {leave_type}')
                    with colb2:
                        leave_count = user_leave_data_collection.count_documents({
                            'start': {
                                '$gte': f'{current_year}-01-01',
                                '$lte': f'{current_year}-12-31'},
                            'user': fname,
                            'type': leave_type})

                        st.markdown(f'###### {leave_count}')
                    with colb3:
                        st.markdown(f"###### {leave_credits_document[leave_type]-leave_count}")
                except:
                    pass

        tab1, tab2 = st.tabs(['Leave Application', 'Leave Cancelation'])
        with tab1:
            st.markdown("### Leave Application")
            gradient_line()

            if team_role != 'Member':
                member_apply = st.checkbox(
                    label='Member Application')
                
                if member_apply:
                    docs = user_collection.find({
                        'team':team,
                        'team_role':'Member'})
                    
                    member_list = []
                    
                    for doc in docs:
                        member_list.append(doc['name'])
                    
                    st.selectbox(
                        label='Select Member',
                        options=member_list,
                        placeholder='Select Member',
                        index=None,
                        key='member_name')
                    
                    fname = st.session_state['member_name']

            st.selectbox(
                label="Select Leave Type",
                options=leave_types,
                key='leave_type_selectbox',
                index=None,
                placeholder='Select Leave Type',)
            st.date_input(
                label="Select Leave Date",
                key='leave_date_input')
            st.text_area(
                label="Reason for Leave",
                key='leave_reason_textarea')
            st.button(
                label="Submit Leave Application",
                key='submit_leave_button',
                use_container_width='stretch')
        with tab2:
            st.markdown("### Leave Cancelation")
            gradient_line()

            # get user leave data documents
            st.write(team_role)
            if team_role != 'Member':
                if team_role == 'Operations Manager':
                    user_leave_data_documents = user_leave_data_collection.find({})
                else:
                    user_leave_data_documents = user_leave_data_collection.find({'team': team})
                df_users_team = pd.DataFrame(user_leave_data_documents)
                if not df_users_team.empty:
                    team_users = df_users_team['user'].unique().tolist()
                    st.selectbox(
                        label='Select Team Member',
                        options=team_users,
                        key='leave_cancel_user_selectbox',
                        index=None,
                        placeholder='Select Team Member to Cancel Leave')
                    
                    team_name = st.session_state.leave_cancel_user_selectbox
                else:
                    team_name = fname  
            else:
                team_name = fname

            user_leave_data_documents = user_leave_data_collection.find({'user': team_name})

            # convert to dataframe
            df = pd.DataFrame(user_leave_data_documents)

            if not df.empty:
                # get available leave types for cancelation
                cancel_leave_types = df['type'].unique().tolist()

                colx, coly = st.columns(2)
                with colx:
                    st.selectbox(
                        label='Leave Type to Cancel',
                        options=cancel_leave_types,
                        key='leave_type_cancel_selectbox',
                        index=None,
                        placeholder='Select Leave Type to Cancel')
                                       
                # get available dates for cancelation based on selected leave type
                cancel_leave_dates = df[df['type'] == st.session_state.leave_type_cancel_selectbox]['start'].unique().tolist()

                with coly:
                    st.selectbox(
                        label='Leave Date to Cancel',
                        options=cancel_leave_dates,
                        key='leave_date_cancel_selectbox',
                        index=None,
                        placeholder='Select Leave Date to Cancel')
                st.button(
                    label="Submit Leave Cancelation",
                    key='submit_leave_cancel_button',
                    use_container_width='stretch')
            else:
                st.markdown("#### No leave applications found to cancel.")
            
            if st.session_state.get('submit_leave_cancel_button'):
                # delete the leave document
                user_leave_data_collection.delete_one({
                    'user': team_name,
                    'type': st.session_state.leave_type_cancel_selectbox,
                    'start': st.session_state.leave_date_cancel_selectbox
                })
                # delete from calendar data collection
                calendar_data_collection = get_collection('calendar_data')
                calendar_data_collection.delete_one({
                    'title': f'{team_name}-{st.session_state.leave_type_cancel_selectbox}',
                    'start': st.session_state.leave_date_cancel_selectbox,
                    'event_type': 'Leave'
                })

                st.rerun()

    with col2:

        # get document from user leave data collection
        collection = get_collection('user_leave_data')

        # get document for all users
        document = collection.find({})

        # convert to dataframe
        df_all_users = pd.DataFrame(document)

        if not df_all_users.empty:
            # rename columns
            df_all_users.rename(columns={'start': 'Date', 'type': 'Leave Type', 'reason': 'Reason', 'user': 'Name', 'team':'Team'}, inplace=True)

            # drop unnecessary columns
            df_all_users.drop(columns=['_id', 'title', 'backgroundColor', 'textColor', 'role', 'event_type'], inplace=True)

            # convert to date
            df_all_users['Date'] = pd.to_datetime(df_all_users['Date'], format='%Y-%m-%d').dt.date

            if team_role in ['Lead', 'Lead-Assistant', 'Operations Manager']:
                tab1, tab2 = st.tabs(['My Logs', 'Team Logs'])
            else:
                tab1, = st.tabs(['My Logs'])

            with tab1:
                # tab for specific user
                st.markdown("### My Leave Data")
                gradient_line()

                # filter dataframe for specific user
                df_fname = df_all_users[df_all_users['Name']==fname]

                if not df_fname.empty:
                    col1, col2 = st.columns([3,1], border=True)

                    with col1:
                        st.dataframe(df_fname, hide_index=True)
                    with col2:
                        df_count = (df_fname['Leave Type']
                            .value_counts()
                            .reset_index(name='Count')
                            .rename(columns={'index': 'Leave Type'}))
                        st.dataframe(df_count, hide_index=True)
                else:
                    st.markdown("#### No leave data found...")
            
            if team_role in ['Lead', 'Lead-Assistant', 'Operations Manager']:
                with tab2:
                    st.markdown("### Team Leave Data")
                    gradient_line()
                    
                    if team=='Management':
                        df_users_team = df_all_users
                    else:
                        df_users_team = df_all_users[df_all_users['Team']==team]

                    if not df_users_team.empty:
                        # filter areas
                        col1, col2 = st.columns(2)
                        with col1:
                            # create a selection box for team members
                            users = set(df_users_team['Name'].to_list())
                            users = sorted(users)
                            select_name = st.selectbox(
                                label='Select Team Member',
                                options=users,
                                placeholder='Select Name',
                                index=None)
                        with col2:
                            # Default date range (optional)
                            current_month = date.today().month
                            default_start = date(date.today().year, current_month, 1)
                            # default_start = date.today()
                            default_end = date.today()

                            select_range=st.date_input(
                                label="Select Leave Date Range",
                                value=(default_start, default_end),
                                # tuple for date range
                                key='leave_date_range')
                            
                        # dataframe areas
                        col1, col2 = st.columns([4,1])
                        with col1:
                            if select_name:
                                df_users_team = df_users_team[df_users_team['Name']==select_name]
                                df_users_team = df_users_team[(df_users_team['Date']>=select_range[0]) & (df_users_team['Date']<=select_range[-1])]
                                st.dataframe(df_users_team, hide_index=True)

                                with col2:
                                    df_count = (df_users_team['Leave Type']
                                        .value_counts()
                                        .reset_index(name='Count')
                                        .rename(columns={'index': 'Leave Type'}))
                                    st.dataframe(df_count, hide_index=True)
                            else:
                                df_users_team = df_users_team[(df_users_team['Date']>=select_range[0]) & (df_users_team['Date']<=select_range[-1])]
                                st.dataframe(df_users_team, hide_index=True)
                    else:
                        st.markdown("#### No team leave data found...")
        
    if st.session_state.get('submit_leave_button'):
        leave_type = st.session_state.leave_type_selectbox
        leave_input = datetime.combine(st.session_state.leave_date_input, time.min)
        leave_date = leave_input.strftime("%Y-%m-%d")
        leave_reason = st.session_state.leave_reason_textarea

        # get leave color
        document = leave_types_collection.find_one({'name': leave_type})
        leave_color = document['color']
        leave_font_color = document['font_color']

        user_leave_data_collection = get_collection('user_leave_data')
        calendar_data_collection = get_collection('calendar_data')

        doc = {'title':f'{fname}-{leave_type}',
               'start': leave_date,
               'backgroundColor': leave_color,
               'textColor': leave_font_color,
               'user': fname,
               'team': team,
               'role': team_role,
               'type': leave_type,
               'reason': leave_reason,
               'event_type': 'Leave'}
        
        exists = user_leave_data_collection.find_one({'user': fname,
                                                      'start': leave_date,
                                                      'type': leave_type})
        
        if exists:
            st.toast("You have already applied for this leave on the selected date.", icon="⚠️")
        else:
            result = user_leave_data_collection.insert_one(doc)
            calendar_data_collection.insert_one({
                'leave_id': str(result.inserted_id),
                'title':f'{fname}-{leave_type}',
                'start': leave_date,
                'backgroundColor': leave_color,
                'textColor': leave_font_color,
                'team': team,
                'event_type': 'Leave'})

        st.rerun()
        st.toast("Leave application submitted!", icon="✅")


    
    

    
