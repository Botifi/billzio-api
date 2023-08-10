from typing import Optional

from httpx import AsyncClient
from .base import BaseBillzHandler
from ..exceptions import *
from ..models.categories import CategoriesListData, CategoriesListFilters
from ..models.products import ProductsListFilters, ProductListData


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
        resp = await self.http_client.get(self._products_route(),
                                          params=filters.model_dump(exclude_unset=True),
                                          headers=self._request_auth_headers())
        json_resp: dict = resp.json()
        if resp.status_code == 200:
            products = ProductListData(**json_resp)
            return products
        else:
            raise ContentRetrieveError

    async def get_categories(self, filters: Optional[CategoriesListFilters]) -> CategoriesListData:
        await self._auth()
        resp = await self.http_client.get(self._categories_route(),
                                          params=filters.model_dump(exclude_unset=True),
                                          headers=self._request_auth_headers())
        json_resp: dict = resp.json()
        if resp.status_code == 200:
            cats = CategoriesListData(**json_resp)
            return cats
        else:
            raise ContentRetrieveError
