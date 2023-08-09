from typing import Any, List, Optional

from pydantic import BaseModel


class SubRow(BaseModel):
    id: str
    name: str
    parent_id: str
    all_parent_ids: Any
    subRows: List["SubRow"]
    product_count: int
    company_id: str
    is_open: bool
    level_number: int
    from_parent: bool
    super_parent_id: str


class Category(BaseModel):
    id: str
    name: str
    parent_id: str
    all_parent_ids: Any
    subRows: List[SubRow]
    product_count: int
    company_id: str
    is_open: bool
    level_number: int
    from_parent: bool
    super_parent_id: str


class CategoriesListData(BaseModel):
    categories: List[Category]
    count: int


class CategoriesListFilters(BaseModel):
    page: Optional[int] = None
    limit: Optional[int] = None
    search: Optional[str] = None
    is_deleted: bool = False
