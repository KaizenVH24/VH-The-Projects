import pandas as pd
import numpy as np
import random

np.random.seed(42)

cities = {
    "Mumbai": 18000,
    "Delhi": 15000,
    "Bengaluru": 12000,
    "Pune": 8000,
    "Hyderabad": 7000,
    "Chennai": 7500,
    "Kolkata": 6000,
    "Ahmedabad": 5500,
    "Jaipur": 5000,
    "Lucknow": 4500
}

location_multiplier = {
    "Premium": 1.3,
    "Standard": 1.0,
    "Developing": 0.8
}

furnishing_bonus = {
    "Furnished": 500000,
    "Semi-Furnished": 250000,
    "Unfurnished": 0
}

data = []

for _ in range(3000):  # 3000 properties
    city = random.choice(list(cities.keys()))
    base_price = cities[city]

    area = random.randint(500, 3000)
    bhk = random.randint(1, 5)
    bathrooms = random.randint(1, 4)
    parking = random.randint(0, 1)
    location = random.choice(list(location_multiplier.keys()))
    age = random.randint(0, 20)
    furnishing = random.choice(list(furnishing_bonus.keys()))

    price = (
        base_price * area *
        location_multiplier[location]
        + bhk * 200000
        + bathrooms * 100000
        + parking * 150000
        - age * 50000
        + furnishing_bonus[furnishing]
    )

    data.append([
        city, area, bhk, bathrooms,
        parking, location, age,
        furnishing, price
    ])

columns = [
    "city", "area_sqft", "bhk",
    "bathrooms", "parking",
    "location_type", "property_age",
    "furnishing", "price"
]

df = pd.DataFrame(data, columns=columns)

df.to_csv("data/housing_data.csv", index=False)

print("Dataset generated successfully!")