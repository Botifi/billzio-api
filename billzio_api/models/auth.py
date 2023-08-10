from pydantic import BaseModel


class AuthLoginData(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int

