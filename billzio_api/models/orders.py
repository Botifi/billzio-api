from typing import List

from pydantic import BaseModel


class NewOrderPayment(BaseModel):
    id: str
    company_payment_type_id: str
    paid_amount: int


class NewOrderProduct(BaseModel):
    id: str
    measurement_value: int


class NewOrderData(BaseModel):
    shop_id: str
    products: List[NewOrderProduct]
    customer_id: str
    payments: List[NewOrderPayment]
