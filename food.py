from common import gradient_line
import streamlit as st
import requests

def food_for_the_soul():
    st.title("Food for the Soul")
    gradient_line()

    col1, col2, col3 = st.columns([2,10,2])    

    with col1:
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
                    width='stretch',
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
                        width='stretch',
                        placeholder='Select Chapter',
                        index=None)
                    

                    url = f"https://bible-api.com/data/web/{book_id}/{chapter_selection}"
                    response = requests.get(url)
                    if response.status_code==200:
                        verses_data = response.json()

                        with col2:
                            st.markdown(f'### {book_seletion} {chapter_selection}')
                            gradient_line()
                            for i in range(len(verses_data['verses'])):
                                st.markdown(f"### :red[[{verses_data['verses'][i]['verse']}]]")
                                st.markdown(f"#### {verses_data['verses'][i]['text']}")
        except:
            pass

                




        







        # st.write(books_data)