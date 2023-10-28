import pytest
import os
from storage import (
    get_user_data, save_user_data, save_category,
    save_purchase, save_balance, get_all_categories,
    get_all_purchases, get_balance
)

STORAGE_PATH = os.getenv("STORAGE_PATH")

@pytest.fixture
def user_id():
    return 123456

@pytest.fixture
async def setup_data(user_id):
    data = {
        "categories": ["Food"],
        "purchases": [{"description": "Burger", "cost": 10.0}],
        "balance": 100.0
    }
    await save_user_data(user_id, data)

@pytest.mark.asyncio
async def test_get_user_data(user_id, setup_data):
    await setup_data
    data = await get_user_data(user_id)
    assert data['categories'] == ['Food']
    assert data['purchases'] == [{"description": "Burger", "cost": 10.0}]
    assert data['balance'] == 100.0

@pytest.mark.asyncio
async def test_save_category(user_id):
    await save_category(user_id, 'Drinks')
    categories = await get_all_categories(user_id)
    assert 'Drinks' in categories

@pytest.mark.asyncio
async def test_save_purchase(user_id):
    purchase = {"description": "Soda", "cost": 2.0}
    await save_purchase(user_id, purchase)
    purchases = await get_all_purchases(user_id)
    assert purchase in purchases

@pytest.mark.asyncio
async def test_save_balance(user_id):
    await save_balance(user_id, 50.0)
    balance = await get_balance(user_id)
    assert balance == 50

@pytest.mark.asyncio
async def test_get_all_categories(user_id, setup_data):
    await setup_data
    categories = await get_all_categories(user_id)
    assert categories == ['Food']

@pytest.mark.asyncio
async def test_get_all_purchases(user_id, setup_data):
    await setup_data
    purchases = await get_all_purchases(user_id)
    assert purchases == [{"description": "Burger", "cost": 10.0}]

@pytest.mark.asyncio
async def test_get_balance(user_id, setup_data):
    await setup_data
    balance = await get_balance(user_id)
    assert balance == 100.0

def teardown_function():
    test_file_path = f'{STORAGE_PATH}123456_data.json'
    if os.path.exists(test_file_path):
        os.remove(test_file_path)
