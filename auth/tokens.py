from joserfc import jwt
from joserfc.jwk import OctKey
from models.user import UserOut

# TODO: change the key for the one in the .env file
key = OctKey.import_key("super_fake_key")


def encode_user_token(user: UserOut):
    encoded_jwt = jwt.encode({"alg": "HS256"}, user.dict(), key)

    return encoded_jwt


def decode_user_token(encoded_jwt: str):
    token = jwt.decode(encoded_jwt, key)

    return token.claims
