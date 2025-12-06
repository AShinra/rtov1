from db import get_collection
from streamlit_calendar import calendar
import streamlit as st


def my_calendar():
    
    events = []
    
    # get user events from db and render calendar
    user_events_collection = get_collection('user_events')
    documents = user_events_collection.find()
    for doc in documents:
        events.extend(doc['events'])

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