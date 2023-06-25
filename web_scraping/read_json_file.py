import json

json_file = 'scraped_data_5.json'

with open(json_file, 'r') as file:
    data = json.load(file)
for property_data in data:
    business_name = property_data['business_name']
    address = property_data['address']
    average_rating = property_data['average_rating']
    total_reviews = property_data['total_reviews']
    staff_rating = property_data['staff_rating']
    facilities_rating = property_data['facilities_rating']
    cleanliness_rating = property_data['cleanliness_rating']
    comfort_rating = property_data['comfort_rating']
    value_for_money_rating = property_data['value_for_money_rating']
    location_rating = property_data['location_rating']
    free_wifi_rating = property_data['free_wifi_rating']
    print(f"Business Name: {business_name}")
    print(f"Address: {address}")
    print(f"Average Rating: {average_rating}")
    print(f"Total Reviews: {total_reviews}")
    print(f"Staff Rating: {staff_rating}")
    print(f"Facilities Rating: {facilities_rating}")
    print(f"Cleanliness Rating: {cleanliness_rating}")
    print(f"Comfort Rating: {comfort_rating}")
    print(f"Value for Money Rating: {value_for_money_rating}")
    print(f"Location Rating: {location_rating}")
    print(f"Free WiFi Rating: {free_wifi_rating}")
    print()

    # uncomment it to read reviews

    reviews = property_data['reviews']
    for review_data in reviews:
        name = review_data['name']
        country_name = review_data['country_name']
        room_type = review_data['room_type']
        review_date = review_data['review_date']
        review_rating = review_data['review_rating']
        review_head = review_data['review_head']
        review_liked = review_data['review_liked']
        review_disliked = review_data['review_disliked']
        print(f"Name: {name}")
        print(f"Country: {country_name}")
        print(f"Room Type: {room_type}")
        print(f"Review Date: {review_date}")
        print(f"Review Rating: {review_rating}")
        print(f"Review Headline: {review_head}")
        print(f"Review Liked: {review_liked}")
        print(f"Review Disliked: {review_disliked}")
        print()
