import json
import random
from datetime import datetime, timedelta

# List of possible categories and descriptions
categories = ["Food", "Guns", "Entertainment", "Clothing", "Electronics", "Health", "Transport"]
descriptions = ["Groceries", "Nerf Gun", "Movie Tickets", "T-Shirt", "Headphones", "Medicine", "Bus Ticket"]

# Initial data
user_data = {
    "categories": categories,
    "purchases": [],
    "balance": 1000.0
}

# Generation of random purchases
current_date = datetime.utcnow() - timedelta(days=365)  # start from a year ago
for i in range(200):  # create 200 purchases
    category = random.choice(categories)
    description = random.choice(descriptions)
    cost = random.uniform(1, 100)  # random cost from 1 to 100
    timestamp = int(current_date.timestamp())
    
    purchase = {
        "description": description,
        "cost": round(cost, 2),  # rounding to 2 decimal places
        "category": category,
        "timestamp": timestamp
    }
    user_data["purchases"].append(purchase)
    
    current_date += timedelta(days=random.randint(0, 3))  # add from 0 to 3 days until the next purchase

# Saving data to a file
user_id = 123456  # your user ID
with open(f'storage/{user_id}_data.json', 'w') as file:
    json.dump(user_data, file, indent=4)
