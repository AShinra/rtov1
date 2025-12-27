from db import get_collection
from streamlit_calendar import calendar
import streamlit as st


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