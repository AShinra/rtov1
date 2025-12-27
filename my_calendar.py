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

    # recurring holidays
    # Jan 1 - New Year's Day, Dec 25 - Christmas Day, Dec 30 - Rizal Day, Jun 12 - Independence Day
    events.append({"title": "New Year's Day","rrule": {"freq": "yearly","bymonth": 1,"bymonthday": 1},"backgroundColor": "red"})
    events.append({"title": "Christmas Day","rrule": {"freq": "yearly","bymonth": 12,"bymonthday": 25},"backgroundColor": "red"})
    events.append({"title": "All Saints Day","rrule": {"freq": "yearly","bymonth": 11,"bymonthday": 1},"backgroundColor": "red"})
    events.append({"title": "Rizal Day","rrule": {"freq": "yearly","bymonth": 12,"bymonthday": 30},"backgroundColor": "red"})
    events.append({"title": "Independence Day","rrule": {"freq": "yearly","bymonth": 6,"bymonthday": 12},"backgroundColor": "red"})

    get_collection('calendar_events')
    company_doc = get_collection('calendar_events').find_one({'team': 'Company'})
    for doc in company_doc['events']:
        events.append(doc)

    # sample formatted events
    # events = [
    #     {"title": "Special Holiday", "start": "2025-12-08", "backgroundColor": "red"},
    #     {"title": "Special Holiday", "start": "2025-12-24", "backgroundColor": "orange"},
    #     {"title": "Special Holiday", "start": "2025-12-31", "backgroundColor": "purple"},
    # ]

    options = {
        "initialView": "dayGridMonth",
        "headerToolbar": {
            "left": "prev,next today",
            "center": "title",
            "right": "dayGridMonth,timeGridWeek"
            },
        }

    calendar(events=events, options=options)


def my_events(team: str):

    # create empty events list
    events = []

    # extract team name if team-lead format
    team = team.split('-')[0]

    if team=='Management':
        calendar_events_collection = get_collection('calendar_events')
        # documents = calendar_events_collection.find({}, {'_id': 0, 'events': 1})
        documents = calendar_events_collection.find({"team":{"$ne":"Company"}})
        for doc in documents:
            events.extend(doc['events'])
    else:
        # get user events from db and render calendar
        calendar_events_collection = get_collection('calendar_events')
        documents = calendar_events_collection.find({'team': team})
        for doc in documents:
            events.extend(doc['events'])
    
    return events

def team_calendar(rights: str, fname: str):

    # get user collection data
    user_collection = get_collection('users')
    user_document = user_collection.find_one({'name': fname})
    calendar_events_collection = get_collection('calendar_events')

    # get related document ids
    role_id, info_id, leave_id, leave_data_id, leave_credits_id, calendar_events_id = get_user_document_ids(user_document)

    # get user role document
    role_collection = get_collection('user_role')
    role_document = role_collection.find_one({'_id': ObjectId(role_id)})

    my_team = role_document['team'].split('-')[0]
    if my_team == 'Management':
        my_team = 'Operations'

    st.title(f"Team Calendar ({my_team})")
    gradient_line()

    if rights == 'admin':
        tab1, tab2 = st.tabs(['📅**Calendar**', '📌**Add Events**'])
    else:
        tab1, = st.tabs(['📅**Calendar**'])

    with tab1:
        my_calendar(role_document['team'])
    
    if rights == 'admin':
        with tab2:
            st.markdown("### Company Holidays")
            gradient_line()
            st.markdown("""
            - **New Year's Day** - January 1
            - **Independence Day** - June 12
            - **All Saints Day** - November 1
            - **Rizal Day** - December 30
            - **Christmas Day** - December 25
            """)

            col1, col2, col3 = st.columns([2, 5, 7])
            with col1:
                st.markdown("#### Add Event")
                gradient_line()
                event_date = st.date_input(
                    label="Select Event Date",
                    key='event_date_input')
                event_title = st.text_input(
                    label="Event Title",
                    key='event_title_input')
                st.button(
                    label="Add Event",
                    key='add_event_button',
                    use_container_width='stretch')
            
            with col2:
                st.markdown("#### Events/Holidays Summary")
                gradient_line()
                company_events_doc = calendar_events_collection.find_one({'team': 'Company'})
                company_events = company_events_doc['events']
                df_events = pd.DataFrame(company_events)
                if not df_events.empty:
                    df_events.drop(columns=['backgroundColor', 'textColor'], inplace=True)
                    df_events.rename(columns={'start': 'Date', 'title': 'Event/Holiday'}, inplace=True)
                    st.dataframe(df_events, hide_index=True)

                else:
                    st.markdown("### No Events to Display")
            
            if st.session_state.get('add_event_button'):
                event_input = datetime.combine(st.session_state.event_date_input, time.min)
                event_date_str = event_input.strftime("%Y-%m-%d")
                event_title_str = st.session_state.event_title_input

                # get company calendar events document
                company_calendar_events_document = calendar_events_collection.find_one({'team': 'Company'})

                result = calendar_events_collection.update_one(
                    {"team": "Company",
                        "events": {
                            "$not": {
                                "$elemMatch": {"title": event_title_str,
                                               "start": event_date_str,
                                               "backgroundColor": "red",
                                               "textColor": "white"}}}},
                                               {"$push": {"events": {
                                                   "title": event_title_str,
                                                   "start": event_date_str,
                                                   "backgroundColor": "red",
                                                   "textColor": "white"}}})
                
                if result.modified_count == 1:
                    st.rerun()
                    st.toast("✅ Event added to calendar!")
                else:
                    st.toast("⚠️ Event already exists")

    