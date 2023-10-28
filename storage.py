import os
from dotenv import load_dotenv
import json

load_dotenv()

STORAGE_PATH = os.getenv("STORAGE_PATH")

async def get_user_data(user_id):
    file_path = f'{STORAGE_PATH}{user_id}_data.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return json.load(file)
    return {"categories": [], "purchases": [], "balance": 0}

async def get_all_categories(user_id):
    user_data = await get_user_data(user_id)
    return user_data.get("categories", [])

async def get_all_purchases(user_id):
    user_data = await get_user_data(user_id)
    return user_data.get("purchases", [])

async def get_balance(user_id):
    user_data = await get_user_data(user_id)
    return user_data.get("balance", 0)

async def save_user_data(user_id, data):
    with open(f'{STORAGE_PATH}{user_id}_data.json', 'w') as file:
        json.dump(data, file)

async def save_category(user_id, category):
    user_data = await get_user_data(user_id)
    if category not in user_data["categories"]:
        user_data["categories"].append(category)
        await save_user_data(user_id, user_data)

async def save_purchase(user_id, purchase):
    user_data = await get_user_data(user_id)
    user_data["purchases"].append(purchase)
    user_data["balance"] -= purchase["cost"]
    await save_user_data(user_id, user_data)

async def save_balance(user_id, balance):
    user_data = await get_user_data(user_id)
    user_data["balance"] += balance
    await save_user_data(user_id, user_data)