from db import get_collection
from streamlit_calendar import calendar
import streamlit as st


def my_calendar(team: str):

    # create empty events list
    events = my_events(team)

    # # extract team name if team-lead format
    # team = team.split('-')[0]

    # if team=='Management':
    #     calendar_events_collection = get_collection('calendar_events')
    #     documents = calendar_events_collection.find({}, {'_id': 0, 'events': 1})
    #     for doc in documents:
    #         events.extend(doc['events'])
    # else:
    #     # get user events from db and render calendar
    #     calendar_events_collection = get_collection('calendar_events')
    #     documents = calendar_events_collection.find({'team': team})
    #     for doc in documents:
    #         events.extend(doc['events'])

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
        documents = calendar_events_collection.find({}, {'_id': 0, 'events': 1})
        for doc in documents:
            events.extend(doc['events'])
    else:
        # get user events from db and render calendar
        calendar_events_collection = get_collection('calendar_events')
        documents = calendar_events_collection.find({'team': team})
        for doc in documents:
            events.extend(doc['events'])
    
    return events