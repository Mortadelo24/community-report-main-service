from fastapi.security import HTTPBearer
from joserfc import jwt
from joserfc.jwk import OctKey
from .models.user import UserToken
from fastapi.encoders import jsonable_encoder
import uuid

security = HTTPBearer()
# TODO: change the key for the one in the .env file
key = OctKey.import_key("super_fake_key")


def encode_user_token(user: UserToken):
    rawUser = user.model_dump()
    rawUser["id"] = str(rawUser["id"])
    encoded_jwt = jwt.encode({"alg": "HS256"},rawUser, key)
    return encoded_jwt

# TODO: check what happen when is sent an invalid token
def decode_user_token(encoded_jwt: str):
    rawUser = jwt.decode(encoded_jwt, key).claims
    rawUser["id"] = uuid.UUID(rawUser["id"])
    return UserToken.model_validate(rawUser)