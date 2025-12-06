import os
from pymongo import MongoClient
import streamlit as st  

_mongo_client = None

@st.cache_resource
def get_client():
    global _mongo_client
    if _mongo_client is None:
        uri = os.environ.get("MongoDB", "mongodb+srv://jonpuray:vYk9PVyQ7mQCn0Rj@cluster1.v4m9pq1.mongodb.net/?retryWrites=true&w=majority&appName=Cluster1")
        _mongo_client = MongoClient(uri, serverSelectionTimeoutMS=5000)
    return _mongo_client

@st.cache_resource
def get_collection(collection_name: str):
    client = get_client()
    db_name = os.environ.get('MMI_DBusers', 'mats')
    db = client[db_name]
    return db[collection_name]

@st.cache_resource
def get_leave_types():
    client = get_client()
    db_name = os.environ.get('MMI_DBusers', 'mats')
    db = client[db_name]
    return db['leave_types']
    


