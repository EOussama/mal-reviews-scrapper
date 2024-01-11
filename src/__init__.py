import requests
from bs4 import BeautifulSoup
import json
import os

def scrape_reviews(user_id):
    base_url = "https://myanimelist.net/profile/{}/reviews".format(user_id)
    all_reviews = []
    page = 1

    while True:
        url = base_url if page == 1 else f"{base_url}?p={page}"
        response = requests.get(url)
        if response.status_code != 200:
            break

        soup = BeautifulSoup(response.content, 'html.parser')
        reviews = soup.find_all("div", class_="borderDark")  # Update this based on the actual class name of the review container

        if not reviews:
            break

        for review in reviews:
            # Extract relevant information from each review here
            review_data = {}
            # Example: review_data['title'] = review.find("a").text
            # Add more fields as needed
            all_reviews.append(review_data)

        page += 1

    return all_reviews

def save_to_json(data, user_id):
    output_dir = f'out/{user_id}'
    os.makedirs(output_dir, exist_ok=True)

    # with open(f'{output_dir}/tt.json', 'w') as f:
    #     json.dump(data, f, indent=4)


if __name__ == '__main__':
  user_id = 'Eoussama'
  reviews = scrape_reviews(user_id)

  save_to_json(reviews, user_id)