
import csv
from bs4 import BeautifulSoup
import requests


# get movies data from imdb
def fetch_data():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0",
        "Accept-Language": "en-US,en;q=0.5"
    }

    response = requests.get('https://www.imdb.com/chart/top/', headers=headers)
    res_txt = response.text

    soup = BeautifulSoup(res_txt, 'html.parser')
    movie_rows = soup.find_all('tr')
    print(f'Found {len(movie_rows)} movies')
    structured_data = process_data(movie_rows)
    return structured_data


# process movie details
def process_data(data):
    movies_list = []

    for row in data:
        try:
            details = row.find('td', class_='titleColumn')
            if details:
                title = details.a.text
                year = int(str(details.span.text).replace(')','').replace('(', ''))
                rate = row.find('td', class_='ratingColumn')
                score = float(rate.strong.text)
                rated = None if not rate.strong['title'] else str(rate.strong['title']).split('on ')[1]
                data = {
                    'title':title,
                    'year':year,
                    'rate':score,
                    'based_on': rated

                }
                movies_list.append(data)
        except Exception as err:
            print(f'Unable to process row number {data.index(row)}, err: {err}')
            continue

    return movies_list


# save processed data into csv file
def save_data(data):
    movies_file = open('movies_list.csv', 'w')
    writer = csv.writer(movies_file)
    writer.writerow(['title', 'year', 'rate','based on'])
    for item in data:
        writer.writerow(item.values())
    movies_file.close()
    print('Movies CSV file generated. Task completed.')


fetch_and_process_movies = fetch_data()
save_movies_list = save_data(fetch_and_process_movies)