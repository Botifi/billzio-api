from typing import Optional, List

from httpx import Client
from .base import BaseBillzHandler
from ..exceptions import *
from ..models.brands import BrandsListData, BrandsListFilters
from ..models.categories import CategoriesListData, CategoriesListFilters
from ..models.clients import ClientsListFilters, ClientsListData, UpsertClientData, NewClientResponse
from ..models.currencies import CurrenciesListData
from ..models.orders import NewOrderData, NewOrderProduct, NewOrderPayment
from ..models.payment_types import PaymentTypesListData
from ..models.products import ProductsListFilters, ProductListData
from ..models.shops import ShopsListFilters, ShopsListData


class BillzHandler(BaseBillzHandler):
    def __init__(self, secret_token: str):
        self.http_client = Client()
        super().__init__(secret_token)
        self._auth()

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
        request_params = filters.model_dump(exclude_unset=True, exclude_none=True) if filters is not None else None
        resp = self.http_client.get(self._products_route(),
                                    params=request_params,
                                    headers=self._request_auth_headers())
        return self._resp_to_model(resp, ProductListData)

    def get_categories(self, filters: Optional[CategoriesListFilters]) -> CategoriesListData:
        request_params = filters.model_dump(exclude_unset=True, exclude_none=True) if filters is not None else None
        resp = self.http_client.get(self._categories_route(),
                                    params=request_params,
                                    headers=self._request_auth_headers())
        return self._resp_to_model(resp, CategoriesListData)

    def get_shops(self, filters: Optional[ShopsListFilters]) -> ShopsListData:
        request_params = filters.model_dump(exclude_unset=True, exclude_none=True) if filters is not None else None
        resp = self.http_client.get(self._shops_route(),
                                    params=request_params,
                                    headers=self._request_auth_headers())
        return self._resp_to_model(resp, ShopsListData)

    def get_currencies(self) -> CurrenciesListData:
        resp = self.http_client.get(self._currencies_route(),
                                    headers=self._request_auth_headers())
        return self._resp_to_model(resp, CurrenciesListData)

    def get_payment_types(self) -> PaymentTypesListData:
        resp = self.http_client.get(self._payment_types_route(),
                                    headers=self._request_auth_headers())
        return self._resp_to_model(resp, PaymentTypesListData)

    def get_brands(self, filters: Optional[BrandsListFilters]) -> BrandsListData:
        request_params = filters.model_dump(exclude_unset=True, exclude_none=True) if filters is not None else None
        resp = self.http_client.get(self._brands_list_route(),
                                    params=request_params,
                                    headers=self._request_auth_headers())
        return self._resp_to_model(resp, BrandsListData)

    def get_clients(self, filters: Optional[ClientsListFilters]) -> ClientsListData:
        request_params = filters.model_dump(exclude_unset=True, exclude_none=True) if filters is not None else None
        resp = self.http_client.get(self._clients_list_create_route(),
                                    params=request_params,
                                    headers=self._request_auth_headers())
        return self._resp_to_model(resp, ClientsListData)

    def create_client(self, data: UpsertClientData) -> NewClientResponse:
        resp = self.http_client.post(self._clients_list_create_route(),
                                     json=data.model_dump(),
                                     headers=self._request_auth_headers())
        return self._resp_to_model(resp, NewClientResponse)

    def update_client(self, client_id: str, data: UpsertClientData) -> bool:
        resp = self.http_client.put(self._clients_detail_route(client_id),
                                    json=data.model_dump(exclude_unset=True, exclude_none=True),
                                    headers=self._request_auth_headers())
        if resp.is_success:
            return True
        else:
            raise ContentUpdateError

    def create_order(self, data: NewOrderData) -> Optional[str]:
        order_id = self._create_draft_order(data.shop_id)
        if order_id:
            for p in data.products:
                self._add_product_to_draft_order(order_id, p)
            self._add_customer_to_draft_order(order_id, data.customer_id)
            self._finish_draft_order(order_id, data.payments)
        return order_id

    def _create_draft_order(self, shop_id: str) -> Optional[str]:
        data = {
            "method": "order.create",
            "params": {
                "shop_id": shop_id
            }
        }
        resp = self.http_client.post(self._orders_list_create_route(),
                                     json=data,
                                     headers=self._request_auth_headers())
        resp_dict = resp.json()
        if resp.is_success:
            if resp_dict.get("result"):
                return resp_dict["result"]
            return None
        else:
            raise ContentCreateError(resp_dict["error"]["message"])

    def _add_product_to_draft_order(self, order_id: str, product: NewOrderProduct) -> bool:
        data = {
            "method": "order.add_item",
            "params": {
                "product_id": product.id,
                "measurement_value": product.measurement_value,
                "order_id": order_id
            }
        }
        resp = self.http_client.post(self._orders_list_create_route(),
                                     json=data,
                                     headers=self._request_auth_headers())

        if resp.is_success:
            return True
        else:
            error = resp.json()
            raise ContentCreateError(error["error"]["message"])

    def _add_customer_to_draft_order(self, order_id: str, customer_id: str) -> bool:
        data = {
            "method": "order.add_customer",
            "params": {
                "customer_id": customer_id,
                "order_id": order_id
            }
        }
        resp = self.http_client.post(self._orders_list_create_route(),
                                     json=data,
                                     headers=self._request_auth_headers())

        if resp.is_success:
            return True
        else:
            error = resp.json()
            raise ContentCreateError(error["error"]["message"])

    def _finish_draft_order(self, order_id: str, payments: List[NewOrderPayment]):
        data = {
            "method": "order.make_payment",
            "params": {
                "payments": [p.model_dump() for p in payments],
                "order_id": order_id
            }
        }
        resp = self.http_client.post(self._orders_list_create_route(),
                                     json=data,
                                     headers=self._request_auth_headers())
        if resp.is_success:
            return True
        else:
            error = resp.json()
            raise ContentCreateError(error["error"]["message"])
