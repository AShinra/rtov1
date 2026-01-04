import streamlit as st
from common import gradient_line
from admin_tools import get_collection
import pandas as pd
from datetime import datetime

def generate_report():
    st.title("Reports")
    gradient_line()

    leave_data_collection = get_collection('user_leave_data')
    leave_data_documents = leave_data_collection.find({})

    df = pd.DataFrame(leave_data_documents)
    df['Month'] = pd.to_datetime(df['start']).dt.month_name()
    df['Year'] = pd.to_datetime(df['start']).dt.year
    

    year_list = set(df['Year'].to_list())

    st.markdown("### Leave Breakdown")
    gradient_line()

    st.selectbox(
        label='Select Year',
        label_visibility='collapsed',
        options=year_list,
        key='year_select',
        placeholder='Select Year',
        index=None,
        width=120)
    
    months = [
        "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    
    months_abr = [
        "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

    teams = [
        'Broadcast', 'Online', 'Print', 'Provincial']
    
    leave_types = [
        'Bereavement', 'Emergency', 'Maternity', 'Others', 'Paternity', 'Sick', 'Vacation']
    
    gradient_line()
    st.markdown(f'##### Team Leave Summary')
    gradient_line()

    col_widths = [2] + [1] * len(months_abr)
    cols = st.columns(col_widths)

    for i, col in enumerate(cols):
        if i==0:
            with col:
                st.markdown(f'###### Team')
                for _team in teams:
                    st.markdown(f'###### {_team}')
        else:
            with col:
                st.markdown(f'###### {months_abr[i-1]}')
                for _team in teams:
                    team_sum = ((df["Month"]==months[i-1]) & (df["Year"]==st.session_state["year_select"]) & (df["team"]==_team)).sum()
                    if team_sum>0:
                        st.markdown(f'###### :red[{team_sum}]')
                    else:
                        st.markdown(f'###### {team_sum}')

    gradient_line()
    st.markdown(f'##### Leave Type Summary')
    gradient_line()

    col_widths = [2] + [1] * len(months_abr)
    cols = st.columns(col_widths)

    for i, col in enumerate(cols):
        if i==0:
            with col:
                st.markdown(f'###### Team')
                for _leave in leave_types:
                    st.markdown(f'###### {_leave}')
        else:
            with col:
                st.markdown(f'###### {months_abr[i-1]}')
                for _leave in leave_types:
                    leave_sum = ((df["Month"]==months[i-1]) & (df["Year"]==st.session_state["year_select"]) & (df["type"]==_leave)).sum()
                    if leave_sum>0:
                        st.markdown(f'###### :red[{leave_sum}]')
                    else:
                        st.markdown(f'###### {leave_sum}')
    
       
    

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

       