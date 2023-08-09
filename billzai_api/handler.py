class AsyncBillzHandler:
    HOST = "https://api-admin.billz.ai"
    AUTH_ROUTE_PATH = "/v1/auth/login"
    PRODUCTS_ROUTE_PATH = "/v2/products"

    def __init__(self, secret_token: str):
        self._secret_token = secret_token
        self.http_client = requests

    def _auth_route(self) -> str:
        return f"{self.HOST}{self.AUTH_ROUTE_PATH}"

    def _products_route(self) -> str:
        return f"{self.HOST}{self.PRODUCTS_ROUTE_PATH}"

    def auth(self):
        self.http_client.post(self._auth_route(), json={"secret_token": self._secret_token})