import firebase_admin
from firebase_admin import credentials, auth


def initialize_firebase():
    try:
        cred = credentials.Certificate("./serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
    except Exception:
        print("Could not initialize firebase")


def get_firebase_uid(token: str):
    try:
        tokenInfo = auth.verify_id_token(token)
    except Exception as e:
        print(e)
        return None

    return tokenInfo["uid"]


async def get_firebase_user(uid: str):
    try:
        user = auth.get_user(uid)
    except Exception as e:
        print(e)
        return None

    return user
