from typing import Optional

import httpx
from pydantic import BaseModel

from billzio_api.exceptions import ContentRetrieveError, ContentCreateError
from billzio_api.models.auth import AuthLoginData


class BaseBillzHandler:
    HOST = "https://api-admin.billz.ai"
    AUTH_ROUTE_PATH = "/v1/auth/login"
    PRODUCTS_ROUTE_PATH = "/v2/products"
    CATEGORIES_ROUTE_PATH = "/v2/category"
    SHOPS_ROUTE_PATH = "/v1/shop"
    CURRENCIES_ROUTE_PATH = "/v2/company-currencies"
    PAYMENT_TYPES_ROUTE_PATH = "/v1/company-payment-type"
    BRANDS_ROUTE_PATH = "/v2/brand"

    CLIENTS_ROUTE_PATH = "/v1/client"
    CLIENT_DETAIL_ROUTE_PATH = "/v1/client/{client_id}"

    ORDER_LIST_CREATE_ROUTE_PATH = "/v1/orders"

    def __init__(self, secret_token: str):
        self._secret_token = secret_token
        self._auth_data: Optional[AuthLoginData] = None

    def _auth(self):
        raise NotImplementedError()

    def _auth_route(self) -> str:
        return f"{self.HOST}{self.AUTH_ROUTE_PATH}"

    def _products_route(self) -> str:
        return f"{self.HOST}{self.PRODUCTS_ROUTE_PATH}"

    def _categories_route(self) -> str:
        return f"{self.HOST}{self.CATEGORIES_ROUTE_PATH}"

    def _shops_route(self) -> str:
        return f"{self.HOST}{self.SHOPS_ROUTE_PATH}"

    def _currencies_route(self) -> str:
        return f"{self.HOST}{self.CURRENCIES_ROUTE_PATH}"

    def _payment_types_route(self) -> str:
        return f"{self.HOST}{self.PAYMENT_TYPES_ROUTE_PATH}"

    def _brands_list_route(self) -> str:
        return f"{self.HOST}{self.BRANDS_ROUTE_PATH}"

    def _clients_list_create_route(self) -> str:
        return f"{self.HOST}{self.CLIENTS_ROUTE_PATH}"

    def _clients_detail_route(self, client_id: str) -> str:
        return f"{self.HOST}{self.CLIENT_DETAIL_ROUTE_PATH.format(client_id=client_id)}"

    def _orders_list_create_route(self) -> str:
        return f"{self.HOST}{self.ORDER_LIST_CREATE_ROUTE_PATH}"

    def _set_auth_data(self, data: dict):
        self._auth_data = AuthLoginData(**data)

    def _request_auth_headers(self) -> dict:
        """ returns header object with Authorization for sending requests """
        request_headers = {
            "Authorization": f"Bearer {self._auth_data.access_token}"
        }
        return request_headers

    def _resp_to_model(self, resp: httpx.Response, scheme):
        json_resp: dict = resp.json()
        if httpx.codes.is_success(resp.status_code):
            products = scheme(**json_resp)
            return products
        else:
            if resp.request.method == "POST":
                raise ContentCreateError
            else:
                raise ContentRetrieveError
