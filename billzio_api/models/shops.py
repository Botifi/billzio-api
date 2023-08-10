from typing import Any, List, Optional

from pydantic import BaseModel


class Shop(BaseModel):
    id: str
    company_id: str
    name: str
    cheque_id: str
    quadrature: int
    phone_numbers: List[str]
    facebook: str
    instagram: str
    telegram: str
    website: str
    has_unique_details: bool
    working_hours: Any
    legal_name: str
    address: str
    legal_country_id: str
    postcode: str
    bank_accounts: List
    cash_boxes: Any
    cash_boxes_count: int
    color: str
    nds: str
    inn: str


class ShopsListData(BaseModel):
    count: int
    shops: List[Shop]


class ShopsListFilters(BaseModel):
    page: Optional[int] = None
    limit: Optional[int] = None

