import streamlit as st
from common import gradient_line, thin_gradient_line, center_num, center_text, center_h5_text, center_h4_text
from admin_tools import get_collection
import pandas as pd
from datetime import datetime

def generate_report():
    st.title("Reports")
    gradient_line()

    leave_data_documents = get_collection('user_leave_data').find({})

    df = pd.DataFrame(leave_data_documents)
    df['Month'] = pd.to_datetime(df['start']).dt.month_name()
    df['Year'] = pd.to_datetime(df['start']).dt.year

    # create a team_list
    leave_data_documents = get_collection('users').find({})
    team_list = []
    for doc in leave_data_documents:
        team_list.append(doc['team'])
    
    teams = sorted(list(set(team_list)))

    year_list = set(df['Year'].to_list())

    st.selectbox(
        label='Select Year',
        label_visibility='collapsed',
        options=year_list,
        key='year_select',
        placeholder='Select Year',
        index=None,
        width=150)
    
    months = [
        "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    
    months_abr = [
        "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    
    leave_types = [
        'Bereavement', 'Emergency', 'Maternity', 'Others', 'Paternity', 'Sick', 'Vacation']
    
    center_h4_text('Leave Summary')
    thin_gradient_line()

    col_widths = [2.5] + [1] * len(months_abr)
    cols = st.columns(col_widths)

    for i, col in enumerate(cols):
        if i==0:
            with col:
                center_text('Team')
                thin_gradient_line()
                for _team in teams:
                    center_text(_team, 'lightblue')
        else:
            with col:
                center_text(months_abr[i-1])
                thin_gradient_line()
                for _team in teams:
                    team_sum = ((df["Month"]==months[i-1]) & (df["Year"]==st.session_state["year_select"]) & (df["team"]==_team)).sum()
                    center_num(team_sum, 'red')
                    
    st.markdown('---')
    center_h4_text('Leave Breakdown')
    thin_gradient_line()

    # create name_list
    name_list = []
    users_documents = get_collection('users').find({})
    for doc in users_documents:
        name_list.append(doc['name'])
    
    name_list = sorted(name_list)
    

    my_columns = ['Name', 'Team', '1st Half VL', '1st Half SL', '1st Half Others', '2nd Half VL', '2nd Half SL', '2nd Half Others']
    first_half = ['January', 'February', 'March', 'April', 'May', 'June']
    second_half = ['July', 'August', 'September', 'October', 'November', 'December']

    col_width = [1.2] + [1]*(len(my_columns)-1)
    cols = st.columns(col_width)

    for i, col in enumerate(cols):
        with col:
            center_text(my_columns[i])
            thin_gradient_line()
            for _name in name_list:
                if i==0:
                    center_text(_name, 'lightblue')
                elif i==1:
                    name_document = get_collection('users').find_one({'name':_name})
                    # st.markdown(f"###### {name_document['team']}")
                    center_text(name_document['team'], 'lightblue')
                elif i==2:
                    leave_sum = ((df["Year"]==st.session_state["year_select"]) & (df["user"]==_name) & (df["Month"].isin(first_half)) & (df['type']=='Vacation')).sum()
                    center_num(leave_sum, 'red')
                elif i==3:
                    leave_sum = ((df["Year"]==st.session_state["year_select"]) & (df["user"]==_name) & (df["Month"].isin(first_half)) & (df['type']=='Sick')).sum()
                    center_num(leave_sum, 'red')
                elif i==4:
                    leave_sum = ((df["Year"]==st.session_state["year_select"]) & (df["user"]==_name) & (df["Month"].isin(first_half)) & (df['type']=='Others')).sum()
                    center_num(leave_sum, 'red')
                elif i==5:
                    leave_sum = ((df["Year"]==st.session_state["year_select"]) & (df["user"]==_name) & (df["Month"].isin(second_half)) & (df['type']=='Vacation')).sum()
                    center_num(leave_sum, 'red')
                elif i==6:
                    leave_sum = ((df["Year"]==st.session_state["year_select"]) & (df["user"]==_name) & (df["Month"].isin(second_half)) & (df['type']=='Sick')).sum()
                    center_num(leave_sum, 'red')
                elif i==7:
                    leave_sum = ((df["Year"]==st.session_state["year_select"]) & (df["user"]==_name) & (df["Month"].isin(second_half)) & (df['type']=='Others')).sum()
                    center_num(leave_sum, 'red')

    



    
    

    
    
       
    

    # with st.container(border=True):
    #     cols = st.columns(len(leave_types)+1)
    #     for i, col in enumerate(cols):
    #         if i==0:
    #             with col:
    #                 st.markdown(f'##### Month')
    #                 for _month in months:
    #                     st.markdown(f'###### {_month}')
    #         else:
    #             with col:
    #                 st.markdown(f'##### {leave_types[i-1]}')
    #                 for _month in months:
    #                     month_sum = ((df["Month"]==_month) & (df["Year"]==st.session_state["year_select"]) & (df["type"]==leave_types[i-1])).sum()
    #                     if month_sum > 0:
    #                         st.markdown(f'###### :red[{month_sum}]')
    #                     else:
    #                         st.markdown(f'###### {month_sum}')

       