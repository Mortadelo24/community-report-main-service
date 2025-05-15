import firebase_admin
from firebase_admin import credentials, auth
from ..models.user import UserFirebase
import os
import dotenv
import json

initialized: bool = False


def initialize():
    global initialized
    if initialized:
        return

    dotenv.load_dotenv()
    try:
        service_credentials = json.loads(os.environ.get("GOOGLE_SERVICE_ACCOUNT"))
        cred = credentials.Certificate(service_credentials)
        firebase_admin.initialize_app(cred)
        print("Firebase was initialized")
        initialized = True
    except Exception:
        print("Could not initialize firebase")


def get_user(token: str) -> UserFirebase | None:
    try:
        tokenInfo = auth.verify_id_token(token)
    except Exception:
        return None

    return UserFirebase(
        display_name=tokenInfo["name"],
        email=tokenInfo["email"],
        id=tokenInfo["uid"]
    )
