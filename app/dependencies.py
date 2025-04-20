from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from .security import security, decode_user_token
from .models.user import UserToken

def get_user_token(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]):
    try:
        return decode_user_token(credentials.credentials)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")



user_token_dependency =  Annotated[UserToken, Depends(get_user_token)]