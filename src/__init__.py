import os
import re
import sys
import json
import requests
import unicodedata
from bs4 import BeautifulSoup


def scrape_reviews(user_id):
    base_url = f'https://myanimelist.net/profile/{user_id}/reviews'
    all_reviews = []
    page = 1

    while True:
        url = base_url if page == 1 else f"{base_url}?p={page}"
        response = requests.get(url)
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        reviews = soup.find_all('div', class_='review-element')

        if not reviews:
            break

        reviews_scrapped = 0
        for review in reviews:
            review_data = {}
            
            review_data['title'] = review.find('a', class_='title').text
            review_data['date'] = review.find('div', class_='update_at').text
            review_data['time'] = review.find('div', class_='update_at')['title']
            review_data['recommmendation'] = review.find('div', class_='tag').text
            review_data['rating'] = int(review.find('div', class_='rating').find('span', class_='num').text)
            review_data['content'] = review.find('div', class_='text').text.replace('\n                  ...\n', '')

            reviews_scrapped += 1
            all_reviews.append(review_data)
            print(f'Scrapped review {reviews_scrapped} of page {page}.')

        page += 1

    return all_reviews

def save_to_json(reviews, user_id):
    output_dir = f'out/{user_id}'
    os.makedirs(output_dir, exist_ok=True)

    for i, review in enumerate(reviews):
        number = len(reviews) - i
        output_name = slugify(f'{number} - {review.get("title")}')
        output_file = f'{output_name}.json'

        with open(f'{output_dir}/{output_file}', 'w') as f:
            json.dump(review, f, indent=4)
    
    print(f'Saved {len(reviews)} review(s) in {output_dir}.')


def slugify(value, allow_unicode=False):
    value = str(value)

    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')

    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')

if __name__ == '__main__':
  user_id = sys.argv[1]
  user_id = user_id if not None else 'Eoussama'

  reviews = scrape_reviews(user_id)

  save_to_json(reviews, user_id)