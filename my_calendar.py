from db import get_collection
from streamlit_calendar import calendar
import streamlit as st
from common import gradient_line, get_user_document_ids
from bson import ObjectId
import pandas as pd
from datetime import datetime, time, date


def my_calendar(team: str):

    # create empty events list
    events = my_events(team)

    # recurring holidays (Jan 1 - New Year's Day, Dec 25 - Christmas Day, Dec 30 - Rizal Day, Jun 12 - Independence Day)
    events.append({"title": "New Year's Day","rrule": {"freq": "yearly","bymonth": 1,"bymonthday": 1},"textColor": "red", "backgroundColor": "black", "event_type": "Holiday"})
    events.append({"title": "Independence Day","rrule": {"freq": "yearly","bymonth": 6,"bymonthday": 12},"textColor": "red", "backgroundColor": "black", "event_type":"Holiday"})
    events.append({"title": "All Saints Day","rrule": {"freq": "yearly","bymonth": 11,"bymonthday": 1},"textColor": "orange", "backgroundColor": "black", "event_type": "Special Non-Working Holiday"})
    events.append({"title": "All Souls Day","rrule": {"freq": "yearly","bymonth": 11,"bymonthday": 2},"textColor": "orange", "backgroundColor": "black", "event_type": "Special Non-Working Holiday"})
    events.append({"title": "Bonifacio Day","rrule": {"freq": "yearly","bymonth": 11,"bymonthday": 30},"textColor": "red", "backgroundColor": "black", "event_type": "Holiday"})
    events.append({"title": "Feast of the Immaculate Conception","rrule": {"freq": "yearly","bymonth": 12,"bymonthday": 8},"textColor": "orange", "backgroundColor": "black", "event_type": "Special Non-Working Holiday"})
    events.append({"title": "Christmas Day","rrule": {"freq": "yearly","bymonth": 12,"bymonthday": 24},"textColor": "orange", "backgroundColor": "black", "event_type": "Special Non-Working Holiday"})
    events.append({"title": "Christmas Day","rrule": {"freq": "yearly","bymonth": 12,"bymonthday": 25},"textColor": "red", "backgroundColor": "black", "event_type": "Holiday"})
    events.append({"title": "Rizal Day","rrule": {"freq": "yearly","bymonth": 12,"bymonthday": 30},"textColor": "red", "backgroundColor": "black", "event_type": "Holiday"})
    events.append({"title": "New Year's Eve","rrule": {"freq": "yearly","bymonth": 12,"bymonthday": 31},"textColor": "orange", "backgroundColor": "black", "event_type": "Special Non-Working Holiday"})
    
    # append birthdays
    documents = get_collection('users').find({})
    for document in documents:
        if document['birthdate']:
            fname = document['name']
            birthdate_month = document['birthdate'].split('-')[1]

            try:
                birthdate_month = int(birthdate_month.lstrip('0'))
            except:
                pass
            
            birthdate_day = document['birthdate'].split('-')[-1]
            
            try:
                birthdate_day = int(birthdate_day.lstrip('0'))
            except:
                pass

            events.append({
                "title": f"{fname}-Birthday",
                "rrule": {"freq": "yearly","bymonth": birthdate_month,"bymonthday": birthdate_day},
                "textColor": "white",
                "backgroundColor": "purple",
                "event_type": "Birthday"
                })
        
    # sample formatted events
    # events = [
    #     {"title": "Special Holiday", "start": "2025-12-08", "backgroundColor": "red"},
    #     {"title": "Special Holiday", "start": "2025-12-24", "backgroundColor": "orange"},
    #     {"title": "Special Holiday", "start": "2025-12-31", "backgroundColor": "purple"},
    # ]

    options = {
        "initialView": "dayGridMonth",
        # "showNonCurrentDates": False,
        # 'eventClick': True,
        # 'dateClick': False,
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek"
            },
        }
    
    st.markdown(':red[▫️Regular Holiday] :orange[▫️Special Non-Working Holiday] :blue[▫️Special Working Holiday] :yellow[▫️Observance] :green[▫️Company Event]')
    calendar(events=events, options=options)


def my_events(team: str):

    # create empty events list
    events = []

    calendar_data_collection = get_collection('calendar_data')
    
    if team == 'Management':
        documents = calendar_data_collection.find({})
    else:
        query = {
            '$or': [
                {'team': team},
                {'team': None}
            ]
        }
        documents = calendar_data_collection.find(query)
        
    for doc in documents:
        events.append({
                "title": doc['title'],
                "start": doc['start'],
                "backgroundColor": doc['backgroundColor'],
                "textColor": doc['textColor']})

    return events

def team_calendar(rights: str, fname: str):

    # get user collection data
    user_collection = get_collection('users')
    user_document = user_collection.find_one({'name': fname})

    # get team and team_role
    team = user_document['team']
    team_role = user_document['team_role']

    # get calendar events collection
    calendar_events_collection = get_collection('calendar_data')

    my_team = team
    if my_team == 'Management':
        my_team = 'Operations'

    st.title(f"Team Calendar ({my_team})")
    gradient_line()

    if rights == 'admin':
        tab1, tab2 = st.tabs(['📅**Calendar**', '📌**Add Events**'])
    else:
        tab1, = st.tabs(['📅**Calendar**'])

    with tab1:
        my_calendar(team)
    
    if rights == 'admin':
        with tab2:
            st.markdown("### Holidays and Events")
            gradient_line()
            colx, coly = st.columns(2)
            with colx:
                st.markdown('#### Recurring Holidays')
                gradient_line()                
                st.markdown(
                        f"""
                        <span style="color:{'red'}">
                        <strong>New Year's Day</strong></span>
                        <span> (Regular Holiday) - January 1</span>""",unsafe_allow_html=True)
                st.markdown(
                        f"""
                        <span style="color:{'red'}">
                        <strong>Independence Day</strong></span>
                        <span> (Regular Holiday) - June 12</span>""",unsafe_allow_html=True)
                st.markdown(
                        f"""
                        <span style="color:{'orange'}">
                        <strong>All Saints Day</strong></span>
                        <span> (Special Non-Working Holiday) - November 1</span>""",unsafe_allow_html=True)
                st.markdown(
                        f"""
                        <span style="color:{'orange'}">
                        <strong>All Souls Day Day</strong></span>
                        <span> (Regular Holiday) - November 2</span>""",unsafe_allow_html=True)
                st.markdown(
                        f"""
                        <span style="color:{'red'}">
                        <strong>Bonifacio Day</strong></span>
                        <span> (Regular Holiday) - November 30</span>""",unsafe_allow_html=True)
                st.markdown(
                        f"""
                        <span style="color:{'orange'}">
                        <strong>Feast of the Immaculate Conception</strong></span>
                        <span> (Special Non-Working Holiday) - December 8</span>""",unsafe_allow_html=True)
                st.markdown(
                        f"""
                        <span style="color:{'orange'}">
                        <strong>Christmas Eve</strong></span>
                        <span> (Special Non-Working Holiday) - December 24</span>""",unsafe_allow_html=True)
                st.markdown(
                        f"""
                        <span style="color:{'red'}">
                        <strong>Christmas Day</strong></span>
                        <span> (Regular Holiday) - December 25</span>""",unsafe_allow_html=True)
                st.markdown(
                        f"""
                        <span style="color:{'red'}">
                        <strong>Rizal Day</strong></span>
                        <span> (Regular Holiday) - December 30</span>""",unsafe_allow_html=True)
                st.markdown(
                        f"""
                        <span style="color:{'orange'}">
                        <strong>New Year's Eve</strong></span>
                        <span> (Special Non-Working Holiday) - December 31</span>""",unsafe_allow_html=True)
                
            
            with coly:
                st.markdown("#### Other Events/Holidays")
                gradient_line()
            
                query = {
                    '$or': [
                        {'event_type': 'Company Event'},
                        {'event_type': 'Observance'},
                        {'event_type': 'Regular Holiday'},
                        {'event_type': 'Special Non-Working Holiday'},
                        {'event_type': 'Special Working Holiday'},
                    ]
                }

                event_documents = calendar_events_collection.find(query)
                for event_document in event_documents:
                    font_color = event_document['textColor']
                    event_title = event_document['title']
                    event_type = event_document['event_type']
                    event_date = datetime.strptime(event_document['start'], "%Y-%m-%d").strftime("%B %d, %Y")

                    st.markdown(
                        f"""
                        <span style="color:{font_color}">
                        <strong>{event_title}</strong></span>
                        <span> ({event_type}) - {event_date}</span>""",unsafe_allow_html=True)
                    

            col1, col2, col3 = st.columns([4, 6, 4])
            with col1:

                event_type_dict = {
                    'Company Event':['green', 'black'],
                    'Observance':['yellow', 'black'],
                    'Regular Holiday':['red', 'black'],
                    'Special Non-Working Holiday':['orange', 'black'],
                    'Special Working Holiday':['blue', 'black']
                }

                # get event type_list
                event_type_list = []
                for event_type, colors in event_type_dict.items():
                    event_type_list.append(event_type)

                st.markdown("#### Add Event")
                gradient_line()
                event_date = st.date_input(
                    label="Select Event Date",
                    key='event_date_input')
                event_title = st.text_input(
                    label="Event Title",
                    key='event_title_input')
                event_type_select = st.selectbox(
                    label="Event Type",
                    options=event_type_list,
                    key='event_type_select_input',
                    placeholder='Select Event Type',
                    index=None)
                st.button(
                    label="Add Event",
                    key='add_event_button',
                    use_container_width='stretch')            
            
            if st.session_state.get('add_event_button'):
                event_input = datetime.combine(st.session_state.event_date_input, time.min)
                event_date_str = event_input.strftime("%Y-%m-%d")
                event_title_str = st.session_state.event_title_input
                event_type_str = st.session_state.event_type_select_input

                exists = calendar_events_collection.find_one(
                    {'title': event_title_str,
                     'start': event_date_str,
                     'event_type': event_type_str})
                
                if not exists:
                    
                    # get event fontcolor and bgcolor
                    font_color = event_type_dict[event_type_str][0]
                    bg_color = event_type_dict[event_type_str][-1]
                    
                    calendar_events_collection.insert_one({
                        'leave_id': None,
                        'title': event_title_str,
                        'start': event_date_str,
                        'backgroundColor': bg_color,
                        'textColor': font_color,
                        'team': None,
                        'event_type': event_type_str
                    })
                    st.rerun()
                    st.toast("✅ Event added to calendar!")
                else:
                    st.toast("⚠️ Event already exists")

                

    