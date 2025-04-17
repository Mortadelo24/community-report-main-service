from apis.firebase import get_firebase_user_from_token
from models.user import UserIn


def get_user_from_firebase(token: str) -> UserIn:
    userInfo = get_firebase_user_from_token(token)

    if not userInfo:
        raise ValueError("Invalid firebase token")

    return UserIn(
        firebase_id=userInfo["uid"],
        display_name=userInfo["name"],
        email=userInfo["email"]
    )
