from typing import Optional

from httpx import AsyncClient
from .base import BaseBillzHandler
from ..exceptions import *
from ..models.categories import CategoriesListData, CategoriesListFilters
from ..models.currencies import CurrenciesListData
from ..models.products import ProductsListFilters, ProductListData
from ..models.shops import ShopsListFilters, ShopsListData


class AsyncBillzHandler(BaseBillzHandler):
    def __init__(self, secret_token: str):
        self.http_client = AsyncClient()
        super().__init__(secret_token)

    async def _auth(self):
        if self._auth_data is None:
            resp = await self.http_client.post(self._auth_route(),
                                               json={"secret_token": self._secret_token})
            json_resp: dict = resp.json()
            if resp.status_code == 200 and json_resp.get("code") == 200 and json_resp.get("data"):
                self._set_auth_data(resp.json()["data"])
            else:
                raise AuthLoginError

    async def get_products(self, filters: Optional[ProductsListFilters]) -> ProductListData:
        await self._auth()
        request_params = filters.model_dump(exclude_unset=True, exclude_none=True) if filters is not None else None
        resp = await self.http_client.get(self._products_route(),
                                          params=request_params,
                                          headers=self._request_auth_headers())
        return self._resp_to_model(resp, ProductListData)

    async def get_categories(self, filters: Optional[CategoriesListFilters]) -> CategoriesListData:
        await self._auth()
        request_params = filters.model_dump(exclude_unset=True, exclude_none=True) if filters is not None else None
        resp = await self.http_client.get(self._categories_route(),
                                          params=request_params,
                                          headers=self._request_auth_headers())
        return self._resp_to_model(resp, CategoriesListData)

    async def get_shops(self, filters: Optional[ShopsListFilters]) -> ShopsListData:
        await self._auth()
        request_params = filters.model_dump(exclude_unset=True, exclude_none=True) if filters is not None else None
        resp = await self.http_client.get(self._shops_route(),
                                          params=request_params,
                                          headers=self._request_auth_headers())
        return self._resp_to_model(resp, ShopsListData)

    async def get_currencies(self) -> CurrenciesListData:
        await self._auth()
        resp = await self.http_client.get(self._currencies_route(),
                                          headers=self._request_auth_headers())
        return self._resp_to_model(resp, CurrenciesListData)
