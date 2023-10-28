from pydantic import BaseModel, confloat

class FundsModel(BaseModel):
    amount: confloat(gt=0)

class PurchaseCostModel(BaseModel):
    cost: confloat(gt=0)