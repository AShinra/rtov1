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

        
        # with tab1:
        #     st.subheader("✍️Add User")
        #     gradient_line()

        #     cola, colb = st.columns(2, border=True)
        #     with cola:
        #         st.subheader("User Info")
        #         gradient_line()
        #         st.text_input(
        #             label="**Username**",
        #             key='add_user_name_input',
        #             placeholder='Enter Username')

        #         st.text_input(
        #             label="**Password**",
        #             type="password",
        #             key='add_user_password_input',
        #             placeholder='Enter Password')
                
        #         st.text_input(
        #             label="**Full Name**",
        #             key='add_user_fname_input',
        #             placeholder='Enter Full Name')
                
        #         st.selectbox(
        #             label="**Permission**",
        #             options=['user', 'admin'],
        #             placeholder='Select Permission',
        #             key='add_user_permission_selectbox',
        #             index=None)
        #     with colb:
        #         departments = ['Operations']
        #         teams = ['Broadcast', 'Online', 'Print', 'Provincial']
        #         roles = ['Lead', 'Lead-Assistant', 'Member']
                
        #         st.subheader("Role Info")
        #         gradient_line()
        #         st.selectbox(
        #             label="**Department**",
        #             options=departments,
        #             placeholder='Select Department',
        #             key='add_user_department_selectbox',
        #             index=None)

        #         st.selectbox(
        #             label="**Team**",
        #             options=teams,
        #             placeholder='Select Team',
        #             key='add_user_team_selectbox',
        #             index=None)
                
        #         st.selectbox(
        #             label="**Team-Role**",
        #             options=roles,
        #             placeholder='Select Team-Role',
        #             key='add_user_role_selectbox',
        #             index=None)
                
        #     st.button(
        #         label="Add User",
        #         width='stretch',
        #         key='add_user_button')
            

        with tab2:
            st.subheader("🔎View Users")
            gradient_line()

            # get user collection
            collection = get_collection('users')
            documents = collection.find({})
            
            # create dataframe
            df = pd.DataFrame(documents)

            # rename columns
            df.rename(columns={'name': 'Full Name', 'department': 'Department', 'team': 'Team', 'team_role': 'Team Role'}, inplace=True)
            
            # display dataframe
            st.dataframe(df[['Full Name', 'Department', 'Team', 'Team Role']], hide_index=True)
        
        with tab3:
            st.subheader("🪪Leave Credits")
            gradient_line()
            col1, col2 = st.columns(2)
            
            user_list = []
            documents = get_collection('users').find()
            for document in documents:
                user_list.append(document['name'])
            
            # sort alphabetically
            user_list = sorted(user_list)
            
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

                    cola, colb = st.columns([3,1])
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
                
                with col2:
                    
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
                    
                    # Submit adjustments in leave credits
                    if submit_adjustments:
                        # update leave credit document
                        leave_credits_collection = get_collection('leave_credits')

                        leave_credits_collection.update_one(
                            {'_id':ObjectId(user_leave_credits_id)},
                            {'$set':{
                                'Sick':sick_data,
                                'Vacation': vacation_data,
                                'Others': others_data,
                                'Birthday': birthday_data,
                                'Bereavement': bereavement_data,
                                'Emergency': emergency_data,
                                'Maternity': matertiny_data,
                                'Paternity': paternity_data}})
                        
                        st.rerun()
            



    with col2:
        ''''''
        
    
    # if st.session_state['add_user_button']:
        
    #     # get user leave data collection
    #     collection = get_collection('user_leave_data')
        
    #     # create leave credit document
    #     leave_credits_collection = get_collection('leave_credits')
    #     leave_credits_doc = {
    #         'Sick':10,
    #         'Vacation':10,
    #         'Others':0,
    #         'Birthday':1,
    #         'Bereavement':3,
    #         'Emergency':2,
    #         'Maternity':0,
    #         'Paternity':0}
        
    #     leave_credits_collection.insert_one(leave_credits_doc)
    #     leave_credits_id = leave_credits_doc['_id']
        
    #     # hash password
    #     ph = PasswordHasher()
    #     hashed_password = ph.hash(st.session_state.get('add_user_password_input'))

    #     user_info = {
    #         'username': st.session_state.get('add_user_name_input'),
    #         'name': st.session_state.get('add_user_fname_input'),
    #         'password_hash': hashed_password,
    #         'rights': st.session_state.get('add_user_permission_selectbox'),
    #         'leave_credits': leave_credits_id,
    #         'department': st.session_state.get('add_user_department_selectbox'),
    #         'team': st.session_state.get('add_user_team_selectbox'),
    #         'team-role': st.session_state.get('add_user_role_selectbox'),
    #         'address': '',
    #         'mobile_number': '',
    #         'birthdate': ''}
        
    #     user_collection = get_collection('users')
    #     user_collection.insert_one(user_info)

    #     st.toast("User added successfully!")
    

    


            
            
                

                    

                
                

            

