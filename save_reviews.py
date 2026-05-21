import json


def save_reviews_to_json(reviews, filename="reviews.json"):

    with open(filename, "w", encoding="utf-8") as f:

        json.dump(reviews, f, indent=4, ensure_ascii=False)

    print(f"\nReviews saved to {filename}") 