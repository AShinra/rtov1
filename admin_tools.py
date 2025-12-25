import streamlit as st
from common import gradient_line
from db import get_collection
from argon2 import PasswordHasher
import pandas as pd
from bson import ObjectId

def user_management():
    st.title("User Management")

    col1, col2 = st.columns([2, 3])

    with col1:
        # Add User
        gradient_line()

        tab1, tab2, tab3 = st.tabs(["✍️**Add User**", "🔎**View Users**", "🪪Leave Credits"])

        
        with tab1:
            st.subheader("✍️Add User")
            gradient_line()

            cola, colb = st.columns(2, border=True)
            with cola:
                st.subheader("User Info")
                gradient_line()
                st.text_input(
                    label="**Username**",
                    key='add_user_name_input',
                    placeholder='Enter Username')

                st.text_input(
                    label="**Password**",
                    type="password",
                    key='add_user_password_input',
                    placeholder='Enter Password')
                
                st.text_input(
                    label="**Full Name**",
                    key='add_user_fname_input',
                    placeholder='Enter Full Name')
                
                st.selectbox(
                    label="**Permission**",
                    options=['user', 'admin'],
                    placeholder='Select Permission',
                    key='add_user_permission_selectbox',
                    index=None)
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
                    key='add_user_department_selectbox',
                    index=None)

                st.selectbox(
                    label="**Team**",
                    options=roles,
                    placeholder='Select Team',
                    key='add_user_team_selectbox',
                    index=None)
                
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
        
        with tab3:
            st.subheader("🪪Leave Credits")
            gradient_line()
            col1, col2 = st.columns(2)
            
            user_list = []
            documents = get_collection('users').find()
            for document in documents:
                user_list.append(document['name'])
            
            with col1:
                selected_name = st.selectbox(
                    label='Name',
                    options=user_list,
                    placeholder='Select Name',
                    index=None)
            
            if selected_name:   
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader('Available Leave')
                    gradient_line()

                    document = get_collection('users').find_one(
                        {'name':selected_name})
                                        
                    user_leave_credits_id = document['leave_credits']
                    
                    document = get_collection('leave_credits').find_one(
                        {'_id':ObjectId(user_leave_credits_id)})
                    
                    sick = document['Sick']
                    vacation = document['Vacation']
                    others = document['Others']
                    birthday = document['Birthday']
                    bereavement = document['Bereavement']
                    emergency = document['Emergency']
                    maternity = document['Maternity']
                    paternity = document['Paternity']

                    cola, colb = st.columns(2)
                    with cola:
                        st.markdown('##### Sick :')
                        st.markdown('##### Vacation :')
                        st.markdown('##### Others :')
                        st.markdown('##### Birthday :')
                        st.markdown('##### Bereavement :')
                        st.markdown('##### Emergency :')
                        st.markdown('##### Maternity :')
                        st.markdown('##### Paternity :')
                    with colb:
                        st.markdown(f'##### {sick}')
                        st.markdown(f'##### {vacation}')
                        st.markdown(f'##### {others}')
                        st.markdown(f'##### {birthday}')
                        st.markdown(f'##### {bereavement}')
                        st.markdown(f'##### {emergency}')
                        st.markdown(f'##### {maternity}')
                        st.markdown(f'##### {paternity}')
                    
                    button_adjust = st.button(
                        label='Adjust',
                        width='stretch')
                
                with col2:
                    if button_adjust:
                        st.subheader('Leave Adjustment')
                        gradient_line()

                        cola, colb = st.columns(2)
                        with cola:
                            st.markdown('##### Sick')
                            sick_data = st.number_input(
                                label='Sick',
                                label_visibility='collapsed',
                                value=sick,
                                step=1,
                                max_value=10,
                                min_value=0)
                            
                            st.markdown('##### Vacation')
                            vacation_data = st.number_input(
                                label='Vacation',
                                label_visibility='collapsed',
                                value=vacation,
                                step=1,
                                max_value=10,
                                min_value=0)
                            
                            st.markdown('##### Others')
                            others_data = st.number_input(
                                label='Others',
                                label_visibility='collapsed',
                                value=others,
                                step=1,
                                max_value=30,
                                min_value=0)
                            
                            st.markdown('##### Birthday')
                            birthday_data = st.number_input(
                                label='Birthday',
                                label_visibility='collapsed',
                                value=birthday,
                                step=1,
                                max_value=1,
                                min_value=0)
                            
                        with colb:
                            st.markdown('##### Bereavement')
                            bereavement_data = st.number_input(
                                label='Bereavement',
                                label_visibility='collapsed',
                                value=bereavement,
                                step=1,
                                max_value=3,
                                min_value=0)
                            
                            st.markdown('##### Emergency')
                            emergency_data = st.number_input(
                                label='Emergency',
                                label_visibility='collapsed',
                                value=emergency,
                                step=1,
                                max_value=2,
                                min_value=0)
                            
                            st.markdown('##### Maternity')
                            matertiny_data = st.number_input(
                                label='Maternity',
                                label_visibility='collapsed',
                                value=maternity,
                                step=1,
                                max_value=60,
                                min_value=0)
                            
                            st.markdown('##### Paternity')
                            paternity_data = st.number_input(
                                label='Paternity',
                                label_visibility='collapsed',
                                value=paternity,
                                step=1,
                                max_value=5,
                                min_value=0)
                        

                    submit_adjustments = st.button(
                        label='Submit Adjustments',
                        width='stretch')
            



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
            
            
                

                    

                
                

            

