from __future__ import annotations

from typing import Any, List, Optional

from pydantic import BaseModel


class Currency(BaseModel):
    type: str
    code: str


class CurrencyRate(BaseModel):
    source_currency: str
    target_currency: str
    rate: int


class CurrenciesListData(BaseModel):
    company_id: str
    supply_currencies: List[Currency]
    retail_currency: Currency
    cross_currencies: Any
    additional_currencies: List[Currency]
    currency_rates: List[CurrencyRate]
