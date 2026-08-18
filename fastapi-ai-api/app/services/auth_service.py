from app.core.security import create_access_token
from app.helpers.auth_helpers import verify_password
from app.services.user_service import get_user_by_email
from app.exceptions.custom import CustomException


def authenticate_user(email: str, password: str):
    try:
        user = get_user_by_email(email)
        if not user:
            raise CustomException(
                status_code=404,
                detail="User not found"
            )
        if not user.is_verified:
            raise CustomException(
                status_code=401,
                detail="User not verified"
            )

        if not verify_password(password, user.password):
            raise CustomException(
                status_code=401,
                detail="Incorrect password"
            )

        access_token = create_access_token(user.id)
        return access_token
    except Exception as e:
        raise CustomException(
            status_code=500,
            detail=str(e)
        )



