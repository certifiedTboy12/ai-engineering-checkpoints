from fastapi import APIRouter
from typing import Any
from app.schemas.auth import UserLogin, AuthResponse
from app.services.auth_service import authenticate_user


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/login", response_model=AuthResponse)
def login_user(request_data: UserLogin) -> dict[str, Any]:

    access_token: str = authenticate_user(request_data.email, request_data.password)

    return {
        "access_token": access_token
    }


