from typing import List, Optional

from pydantic import BaseModel


class Category(BaseModel):
    id: str
    name: str
    parent_id: str


class CustomField(BaseModel):
    custom_field_id: str
    custom_field_value: str


class MeasurementUnit(BaseModel):
    id: str
    name: str
    short_name: str


class ProductAttribute(BaseModel):
    attribute_id: str
    attribute_name: Optional[str]
    attribute_value: str
    attribute_value_id: str


class ShopMeasurementValue(BaseModel):
    active_measurement_value: int
    shop_id: str
    shop_name: str


class ShopPrice(BaseModel):
    retail_currency: str
    retail_price: int
    shop_id: str
    shop_name: str


class Product(BaseModel):
    id: str
    name: str
    barcode: str
    sku: str
    brand_id: str
    brand_name: str
    description: str
    is_variative: bool
    main_image_url: str
    categories: List[Category]
    custom_fields: Optional[List[CustomField]]
    measurement_unit: MeasurementUnit
    parent_id: str
    product_attributes: List[ProductAttribute]
    product_type_id: str
    shop_measurement_values: List[ShopMeasurementValue]
    shop_prices: List[ShopPrice]
    updated_at: str


class ProductListData(BaseModel):
    count: int
    products: List[Product]


class ProductsListFilters(BaseModel):
    page: Optional[int] = None
    limit: Optional[int] = None
    search: Optional[str] = None

