import pytest
import os
from charts import (
    generate_expense_chart, generate_category_chart, 
    generate_distribution_histogram, generate_cumulative_expense_chart,
    generate_weekday_expense_chart, generate_average_expense_per_category_chart
)

user_data = {
    "categories": ["Food", "Drinks"],
    "purchases": [
        {"description": "Burger", "cost": 10.0, "timestamp": 1635204800, "category": "Food"},
        {"description": "Soda", "cost": 2.0, "timestamp": 1635208400, "category": "Drinks"}
    ],
    "balance": 100.0
}

@pytest.mark.asyncio
async def test_generate_expense_chart():
    file_name = await generate_expense_chart(user_data)
    assert os.path.exists(file_name) and file_name.endswith('.png')

@pytest.mark.asyncio
async def test_generate_category_chart():
    file_name = await generate_category_chart(user_data)
    assert os.path.exists(file_name) and file_name.endswith('.png')

@pytest.mark.asyncio
async def test_generate_distribution_histogram():
    file_name = await generate_distribution_histogram(user_data)
    assert os.path.exists(file_name) and file_name.endswith('.png')

@pytest.mark.asyncio
async def test_generate_cumulative_expense_chart():
    file_name = await generate_cumulative_expense_chart(user_data)
    assert os.path.exists(file_name) and file_name.endswith('.png')

@pytest.mark.asyncio
async def test_generate_weekday_expense_chart():
    file_name = await generate_weekday_expense_chart(user_data)
    assert os.path.exists(file_name) and file_name.endswith('.png')

@pytest.mark.asyncio
async def test_generate_average_expense_per_category_chart():
    file_name = await generate_average_expense_per_category_chart(user_data)
    assert os.path.exists(file_name) and file_name.endswith('.png')

def teardown_function():
    for file_name in os.listdir('/tmp'):
        if file_name.endswith('.png'):
            os.remove(os.path.join('/tmp', file_name))
