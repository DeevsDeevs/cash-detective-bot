import pytest
from models import FundsModel, PurchaseCostModel
from pydantic import ValidationError

def test_funds_model():
    valid_data = {"amount": 10.5}
    model = FundsModel(**valid_data)
    assert model.model_dump() == valid_data

    with pytest.raises(ValidationError) as exc_info:
        FundsModel(amount=-10.5)
    assert exc_info.value.errors() == [
        {
            "loc": ("amount",),
            "msg": "Input should be greater than 0",
            "type": "greater_than",
            "ctx": {"gt": 0.0},
            'input': -10.5,
            'url': 'https://errors.pydantic.dev/2.3/v/greater_than'
        }
    ]

def test_purchase_cost_model():
    valid_data = {"cost": 20.0}
    model = PurchaseCostModel(**valid_data)
    assert model.model_dump() == valid_data

    with pytest.raises(ValidationError) as exc_info:
        PurchaseCostModel(cost=-20.0)
    assert exc_info.value.errors() == [
        {
            "loc": ("cost",),
            "msg": "Input should be greater than 0",
            "type": "greater_than",
            "ctx": {"gt": 0.0},
            'input': -20,
            'url': 'https://errors.pydantic.dev/2.3/v/greater_than'
        }
    ]
