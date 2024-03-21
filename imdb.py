from bs4 import BeautifulSoup
import requests
import json


def extract_details(genre):
    base_url = 'https://www.imdb.com'
    # fake a browser visit
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    url = f"{base_url}/search/title/?genres={genre}"
    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find(class_='ipc-metadata-list ipc-metadata-list--dividers-between sc-748571c8-0 jmWPOZ detailed-list-view ipc-metadata-list--base')
    movie_data = []

    for j in title:
        movie={}
        movie_title = j.find(class_='ipc-title ipc-title--base ipc-title--title ipc-title-link-no-icon ipc-title--on-textPrimary sc-b0691f29-9 klOwFB dli-title')
        movie_title=movie_title.get_text()
        movie['Title'] = '.'.join(movie_title.split(".")[1:])
        year = j.find(class_='sc-b0691f29-8 ilsLEX dli-title-metadata-item')
        movie['Year'] = year.get_text()
        rating_span = j.find('span', class_='ipc-rating-star--base')
        if rating_span is not None:
            if 'IMDb rating' in rating_span['aria-label']:
                imdb_rating = rating_span['aria-label'].split(': ')[1]
            else:
                imdb_rating = ""    
        else:
            imdb_rating = ""

        movie['Imdb Rating'] = imdb_rating

        movie['Plot Summary'] = j.find(class_='ipc-html-content-inner-div').get_text()

        movie_data.append(movie)

        return movie_data


def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    print("Welcome to IMDB Website !!")
    genre = input("Enter specific genre for searching: ")
    page_no = input("Enter number of pages you want to see: ")
    movie_data = extract_details(genre)

    save_to_json(movie_data, 'movies.json')