from pydantic import BaseModel, HttpUrl
from typing import Literal

class TokenBase(BaseModel):
    access_token: str
    token_type: Literal["Bearer"]    

class TokenCreate(TokenBase):
    provider: Literal["google"] 
    refresh_token: str | None = None
    scope: HttpUrl | None = None

class TokenResponse(TokenBase):
    pass