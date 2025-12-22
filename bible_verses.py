import requests
import random

def get_random_bible_verse():
    books = [
        "Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy",
        "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
        "Matthew", "Mark", "Luke", "John", "Romans",
        "1 Corinthians", "2 Corinthians", "Galatians",
        "Ephesians", "Philippians", "Colossians"
    ]

    book = random.choice(books)
    chapter = random.randint(1, 150)
    verse = random.randint(1, 176)

    url = f"https://bible-api.com/{book}%20{chapter}:{verse}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return f"{data['reference']} — {data['text'].strip()}"
    else:
        return "Luke 4:10 — for it is written,‘He will put his angels in charge of you, to guard you;’"
    

# Example usage
# print(get_random_bible_verse())
