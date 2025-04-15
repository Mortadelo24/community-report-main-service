import firebase_admin
from firebase_admin import credentials, auth


def initialize_firebase():
    try:
        cred = credentials.Certificate("./serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
    except Exception:
        print("Could not initialize firebase")


def isAuthTokenValid(token: str):
    try:
        print(auth.verify_id_token(token))
        return True
    except Exception:
        return False
