from typing import Optional

from billzai_api.models.auth import AuthLoginData


class BaseBillzHandler:
    HOST = "https://api-admin.billz.ai"
    AUTH_ROUTE_PATH = "/v1/auth/login"
    PRODUCTS_ROUTE_PATH = "/v2/products"

    def __init__(self, secret_token: str):
        self._secret_token = secret_token
        self._auth_data: Optional[AuthLoginData] = None

    def _auth_route(self) -> str:
        return f"{self.HOST}{self.AUTH_ROUTE_PATH}"

    def _products_route(self) -> str:
        return f"{self.HOST}{self.PRODUCTS_ROUTE_PATH}"

    def _set_auth_data(self, data: dict):
        self._auth_data = AuthLoginData(**data)

    def _request_auth_headers(self) -> dict:
        """ returns header object with Authorization for sending requests """
        request_headers = {
            "Authorization": f"Bearer {self._auth_data.access_token}"
        }
        return request_headers
