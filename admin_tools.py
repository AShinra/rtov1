import streamlit as st
from common import gradient_line
from db import get_collection
from argon2 import PasswordHasher
import pandas as pd

def user_management():
    st.title("User Management")

    col1, col2 = st.columns([2, 3])

    with col1:
        # Add User
        gradient_line()

        tab1, tab2 = st.tabs(["✍️**Add User**", "🔎**View Users**"])

        
        with tab1:
            st.subheader("✍️Add User")
            gradient_line()

            cola, colb = st.columns(2, border=True)
            with cola:
                st.subheader("User Info")
                gradient_line()
                st.text_input(
                    label="**Username**",
                    key='add_user_name_input')

                st.text_input(
                    label="**Password**",
                    type="password",
                    key='add_user_password_input')
                
                st.text_input(
                    label="**Full Name**",
                    key='add_user_fname_input')
                
                st.selectbox(
                    label="**Permission**",
                    options=['user', 'admin'],
                    placeholder='Select Permission',
                    key='add_user_permission_selectbox')
            with colb:
                departments = []
                roles = []
                role_collection = get_collection('user_role')

                # get unique departments and teams
                for department_doc in role_collection.find({}, {'_id': 0, 'department': 1}):
                    departments.append(department_doc['department'])

                departments = list(set(departments))

                for role_doc in role_collection.find({}, {'_id': 0, 'team': 1}):
                    roles.append(role_doc['team'])

                roles = list(set(roles))

                st.subheader("Role Info")
                gradient_line()
                st.selectbox(
                    label="**Department**",
                    options=departments,
                    placeholder='Select Department',
                    key='add_user_department_selectbox')

                st.selectbox(
                    label="**Team**",
                    options=roles,
                    placeholder='Select Team',
                    key='add_user_team_selectbox')
                
            st.button(
                label="Add User",
                width='stretch',
                key='add_user_button')
            

        with tab2:
            st.subheader("🔎View Users")
            gradient_line()

            # get user collection
            collection = get_collection('users')
            documents = collection.find({})
            
            # create dataframe
            df = pd.DataFrame(documents)

            # remove other columns
            df.drop(columns=['_id', 'password_hash', 'user_info', 'leave_credits', 'leave_data', 'user_events', 'role'], inplace=True)
            
            st.dataframe(df)



    with col2:
        ''''''
        
    
    if st.session_state['add_user_button']:
        
        # get role id
        role_collection = get_collection('user_role')
        doc = role_collection.find_one(
            {
                'department': st.session_state.get('add_user_department_selectbox'),
                'team': st.session_state.get('add_user_team_selectbox')
            },
            {'_id': 1})
        
        role_id = doc['_id']

        # create leave_data document
        leave_data_collection = get_collection('leave_data')
        leave_data_doc = {
            'Vacation': [],
            'Others': [],
            'Sick': [],
            'Birthday': [],
            'Bereavement': [],
            'Emergency': [],
            'Maternity': [],
            'Paternity': [],
        }

        leave_data_collection.insert_one(leave_data_doc)
        leave_data_id = leave_data_doc['_id']

        # create a user event id
        user_events_collection = get_collection('calendar_events')
        _team = st.session_state['add_user_team_selectbox']
        _team = _team.split('-')[0]  # extract team name if team-lead format

        doc = user_events_collection.find_one(
            {
                'team': _team
            },
            {'_id': 1})
        
        user_events_id = doc['_id']

        # create a user info document
        user_info_collection = get_collection('users_info')
        user_info_doc = {
            'address':'No Address given - Please update',
            'mobile_number':'No Phone Number given - Please update'
        }

        user_info_collection.insert_one(user_info_doc)
        user_info_id = user_info_doc['_id']

        # create leave credit document
        leave_credits_collection =get_collection('leave_credits')
        leave_credits_doc = {
            'Sick':0,
            'Vacation':0,
            'Others':0,
            'Birthday':0,
            'Bereavement':0,
            'Emergency':0,
            'Maternity':0,
            'Paternity':0
            }
        
        leave_credits_collection.insert_one(leave_credits_doc)
        leave_credits_id = leave_credits_doc['_id']
        
        # hash password
        ph = PasswordHasher()
        hashed_password = ph.hash(st.session_state.get('add_user_password_input'))

        user_info = {
            'username': st.session_state.get('add_user_name_input'),
            'name': st.session_state.get('add_user_fname_input'),
            'password_hash': hashed_password,
            'rights': st.session_state.get('add_user_permission_selectbox'),
            'role': role_id,
            'leave_data': leave_data_id,
            'user_events': user_events_id,
            'user_info': user_info_id,
            'leave_credits': leave_credits_id
        }
        user_collection = get_collection('users')
        user_collection.insert_one(user_info)

        st.toast("User added successfully!")
            
            
                

                    

                
                

            

