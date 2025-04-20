import firebase_admin
from firebase_admin import credentials, auth
from ..models.user import UserFirebase

initialized: bool = False

def initialize():
    global initialized
    if initialized == True:
        return
    
    try:
        cred = credentials.Certificate("./serviceAccountKey.json")
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
        id= tokenInfo["uid"]
    )
