import firebase_admin
from firebase_admin import credentials, auth


def initialize_firebase():
    try:
        cred = credentials.Certificate("./serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
    except Exception:
        print("Could not initialize firebase")


def get_firebase_user_from_token(token: str):
    try:
        tokenInfo = auth.verify_id_token(token)
    except Exception:
        return None

    return tokenInfo


def get_firebase_user(uid: str):
    try:
        user = auth.get_user(uid)
    except Exception:
        return None

    return user


def get_firebase_uid(token: str):
    tokenInfo = get_firebase_user_from_token(token)
    if not tokenInfo:
        return None

    return tokenInfo["uid"]
