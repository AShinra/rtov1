from common import gradient_line
import streamlit as st
import requests

def food_for_the_soul():
    st.title("Food for the Soul")
    gradient_line()

    try:
        # get books
        url = f"https://bible-api.com/data/web"
        response = requests.get(url)

        if response.status_code == 200:
            books_data = response.json()

            books = []
            for i in range(len(books_data['books'])):
                books.append(books_data['books'][i]['name'])
            
            book_seletion = st.selectbox(
                label='Select Book',
                options=books,
                width=250,
                placeholder='Select Book',
                index=None)
            
            for i in range(len(books_data['books'])):
                if books_data['books'][i]['name']==book_seletion:
                    book_id = books_data['books'][i]['id']
                    break
            
            url = f"https://bible-api.com/data/web/{book_id}"
            response = requests.get(url)
            if response.status_code==200:
                chapters_data = response.json()

                chapters = len(chapters_data['chapters'])
                
                chapter_selection = st.selectbox(
                    label='Select Chapter',
                    options=range(1, chapters+1),
                    width=250,
                    placeholder='Select Chapter',
                    index=None)
                

                url = f"https://bible-api.com/data/web/{book_id}/{chapter_selection}"
                response = requests.get(url)
                if response.status_code==200:
                    verses_data = response.json()

                    col1, col2 = st.columns([1,10])
                    with col2:
                        st.markdown(f'### {book_seletion} {chapter_selection}')
                        for i in range(len(verses_data['verses'])):
                            st.write(f"[{verses_data['verses'][i]['verse']}] {verses_data['verses'][i]['text']}")

    except:
        pass

                




        







        # st.write(books_data)