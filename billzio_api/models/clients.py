from enum import Enum
from typing import Optional, List

from pydantic import BaseModel


class Client(BaseModel):
    id: str
    external_id: str
    first_name: str
    last_name: str
    middle_name: str
    created_at: str
    birth_date: str
    first_transaction_date: str
    last_transaction_date: str
    balance: int
    cards: List
    company_name: str
    phone_numbers: List[str]
    gender: str


class ClientsListData(BaseModel):
    count: int
    clients: List[Client]


class ClientsListFilters(BaseModel):
    page: Optional[int] = None
    limit: Optional[int] = None
    search: Optional[str] = None
    phone_number: Optional[str] = None
    chat_id: Optional[str] = None  # chat_id in Telegram messenger


class ClientGenderEnum(int, Enum):
    not_set = 0
    male = 1
    female = 2


class UpsertClientData(BaseModel):
    chat_id: Optional[str] = None  # chat_id in Telegram messenger
    date_of_birth: Optional[str] = None  # format 2022-05-14
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[ClientGenderEnum] = None
    phone_number: Optional[str] = None


class NewClientResponse(BaseModel):
    id: str
