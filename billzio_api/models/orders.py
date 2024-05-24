from typing import List, Optional

from pydantic import BaseModel


class NewOrderPayment(BaseModel):
    id: str
    company_payment_type_id: str
    paid_amount: int | float


class NewOrderProduct(BaseModel):
    id: str
    measurement_value: int | float


class NewOrderData(BaseModel):
    shop_id: str
    products: List[NewOrderProduct]
    customer_id: str
    payments: Optional[List[NewOrderPayment]]
