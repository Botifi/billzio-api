from typing import List

from pydantic import BaseModel


class PaymentType(BaseModel):
    id: str
    name: str


class CompanyPaymentType(BaseModel):
    id: str
    company_id: str
    payment_type: PaymentType
    token: str
    name: str
    is_editable: bool


class PaymentTypesListData(BaseModel):
    company_payment_types: List[CompanyPaymentType]
    count: int
