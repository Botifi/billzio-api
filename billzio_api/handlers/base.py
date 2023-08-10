from typing import Optional

from billzio_api.models.auth import AuthLoginData


class BaseBillzHandler:
    HOST = "https://api-admin.billz.ai"
    AUTH_ROUTE_PATH = "/v1/auth/login"
    PRODUCTS_ROUTE_PATH = "/v2/products"
    CATEGORIES_ROUTE_PATH = "/v2/category"
    SHOPS_ROUTE_PATH = "/v1/shop"
    CURRENCIES_ROUTE_PATH = "/v2/company-currencies"

    def __init__(self, secret_token: str):
        self._secret_token = secret_token
        self._auth_data: Optional[AuthLoginData] = None

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

    def _set_auth_data(self, data: dict):
        self._auth_data = AuthLoginData(**data)

    def _request_auth_headers(self) -> dict:
        """ returns header object with Authorization for sending requests """
        request_headers = {
            "Authorization": f"Bearer {self._auth_data.access_token}"
        }
        return request_headers
