from typing import Optional

from httpx import AsyncClient, Client
from .base import BaseBillzHandler
from ..exceptions import *
from ..models.categories import CategoriesListData, CategoriesListFilters
from ..models.currencies import CurrenciesListData
from ..models.products import ProductsListFilters, ProductListData
from ..models.shops import ShopsListFilters, ShopsListData


class BillzHandler(BaseBillzHandler):
    def __init__(self, secret_token: str):
        self.http_client = Client()
        super().__init__(secret_token)

    def _auth(self):
        if self._auth_data is None:
            resp = self.http_client.post(self._auth_route(),
                                         json={"secret_token": self._secret_token})
            json_resp: dict = resp.json()
            if resp.status_code == 200 and json_resp.get("code") == 200 and json_resp.get("data"):
                self._set_auth_data(resp.json()["data"])
            else:
                raise AuthLoginError

    def get_products(self, filters: Optional[ProductsListFilters]) -> ProductListData:
        self._auth()
        request_params = filters.model_dump(exclude_unset=True, exclude_none=True) if filters is not None else None
        resp = self.http_client.get(self._products_route(),
                                    params=request_params,
                                    headers=self._request_auth_headers())
        json_resp: dict = resp.json()
        if resp.status_code == 200:
            products = ProductListData(**json_resp)
            return products
        else:
            raise ContentRetrieveError

    def get_categories(self, filters: Optional[CategoriesListFilters]) -> CategoriesListData:
        self._auth()
        request_params = filters.model_dump(exclude_unset=True, exclude_none=True) if filters is not None else None
        resp = self.http_client.get(self._categories_route(),
                                    params=request_params,
                                    headers=self._request_auth_headers())
        json_resp: dict = resp.json()
        if resp.status_code == 200:
            cats = CategoriesListData(**json_resp)
            return cats
        else:
            raise ContentRetrieveError

    def get_shops(self, filters: Optional[ShopsListFilters]) -> ShopsListData:
        self._auth()
        request_params = filters.model_dump(exclude_unset=True, exclude_none=True) if filters is not None else None
        resp = self.http_client.get(self._shops_route(),
                                    params=request_params,
                                    headers=self._request_auth_headers())
        json_resp: dict = resp.json()
        if resp.status_code == 200:
            shops = ShopsListData(**json_resp)
            return shops
        else:
            raise ContentRetrieveError

    def get_currencies(self) -> CurrenciesListData:
        self._auth()
        resp = self.http_client.get(self._currencies_route(),
                                    headers=self._request_auth_headers())
        json_resp: dict = resp.json()
        if resp.status_code == 200:
            currencies = CurrenciesListData(**json_resp)
            return currencies
        else:
            raise ContentRetrieveError
