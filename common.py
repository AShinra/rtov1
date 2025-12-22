import streamlit as st
import requests

def gradient_line():
    st.markdown("<hr style='border: 0; height: 10px; padding: 0; margin: 0; background: linear-gradient(to right, #444, #bbb);'/>", unsafe_allow_html=True)

def get_logo():
    # Return a path or bytes object for the logo image if you have one.
    return None

def get_random_bible_verse():
    # Return random bible verses
    url = f"https://bible-api.com/data/web/random"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        book = data['random_verse']['book']
        chapter = data['random_verse']['chapter']
        verse = data['random_verse']['verse']
        text = data['random_verse']['text']
        return(f'{book} {chapter}:{verse} - {text}')
    else:
        return "John 3:16 — or God so loved the world, that he gave his only begotten Son, that whosoever believeth in him should not perish, but have everlasting life’"

def get_random_bible_chapters(book: str, chapter: int):
    # Return a random chapter
    url = f"https://bible-api.com/data/web/JHN"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return(data)

