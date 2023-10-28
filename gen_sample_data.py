import json
import random
from datetime import datetime, timedelta

# Список возможных категорий и описаний
categories = ["Food", "Guns", "Entertainment", "Clothing", "Electronics", "Health", "Transport"]
descriptions = ["Groceries", "Nerf Gun", "Movie Tickets", "T-Shirt", "Headphones", "Medicine", "Bus Ticket"]

# Начальные данные
user_data = {
    "categories": categories,
    "purchases": [],
    "balance": 1000.0
}

# Генерация случайных покупок
current_date = datetime.utcnow() - timedelta(days=365)  # начать с года назад
for i in range(200):  # создать 200 покупок
    category = random.choice(categories)
    description = random.choice(descriptions)
    cost = random.uniform(1, 100)  # случайная стоимость от 1 до 100
    timestamp = int(current_date.timestamp())
    
    purchase = {
        "description": description,
        "cost": round(cost, 2),  # округление до 2 знаков после запятой
        "category": category,
        "timestamp": timestamp
    }
    user_data["purchases"].append(purchase)
    
    current_date += timedelta(days=random.randint(0, 3))  # добавить от 0 до 3 дней до следующей покупки

# Сохранение данных в файл
user_id = 123456  # ваш ID пользователя
with open(f'storage/{user_id}_data.json', 'w') as file:
    json.dump(user_data, file, indent=4)
