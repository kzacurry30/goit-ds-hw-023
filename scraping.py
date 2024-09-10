import requests
from bs4 import BeautifulSoup
import json
import time

base_url = "http://quotes.toscrape.com"
author_base_url = "http://quotes.toscrape.com"

quotes_data = []
authors_data = []

def get_author_info(author_url):
    response = requests.get(author_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    full_name = soup.find("h3", class_='author-title').text.strip()
    born_date = soup.find("span", class_="author-born-date").text.strip()
    born_location = soup.find("span", class_="author-born-location").text.strip()
    description = soup.find("div", class_="author-description").text.strip()

    author_info = {
        "full_name": full_name,
        "born_date": born_date,
        "born_location": born_location,
        "description": description
    }

    return author_info


def scrape_quotes():
    page_url = "/page/1/"

    while page_url:
        response = requests.get(base_url + page_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        quotes = soup.find_all('div', class_='quote')

        for quote in quotes:
            text = quote.find('span', class_='text').text
            author_tag = quote.find('small', class_='author')

            if isinstance(author_tag, BeautifulSoup) and author_tag:
                author = author_tag.text
            elif isinstance(author_tag, str):
                author = author_tag
            else:
                author = "Unknown"

            tags = [tag.text for tag in quote.find_all('a', class_='tag')]
            author_url_tag = quote.find('a')

            if author_url_tag:
                author_url = author_url_tag['href']
                # Перевірка наявності ключа 'fullname' перед порівнянням
                if not any(a.get('fullname') == author for a in authors_data):
                    author_info = get_author_info(author_base_url + author_url)
                    authors_data.append(author_info)
            else:
                author_url = None

            quote_data = {
                "quote": text,
                "author": author,
                "tags": tags
            }
            quotes_data.append(quote_data)

        next_button = soup.find('li', class_='next')
        if next_button:
            page_url = next_button.find('a')['href']
        else:
            page_url = None

        time.sleep(1)


scrape_quotes()

with open('quotes.json', 'w', encoding='utf-8') as f:
    json.dump(quotes_data, f, ensure_ascii=False, indent=4)

with open('authors.json', 'w', encoding='utf-8') as f:
    json.dump(authors_data, f, ensure_ascii=False, indent=4)


