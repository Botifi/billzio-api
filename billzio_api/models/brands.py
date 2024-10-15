from typing import List, Optional

from pydantic import BaseModel


class Brand(BaseModel):
    id: str
    name: str
    company_id: str
    logo: str


class BrandsListData(BaseModel):
    count: int
    brands: Optional[List[Brand]]


class BrandsListFilters(BaseModel):
    page: Optional[int] = None
    limit: Optional[int] = None
    search: Optional[str] = None

