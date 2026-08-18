from fastapi import APIRouter, Depends
from app.schemas.user import UserCreate, VerifyOTPRequest, ResendOtpRequest, UserResponse
from app.core.dependencies import get_current_user_id
from app.services.user_service import create_user, verify_user, generate_new_otp, get_user_by_id




router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/", response_model=UserResponse)
def create_new_user(user_data: UserCreate):

    created_user = create_user(user_data.first_name, user_data.last_name, user_data.email, user_data.password)          
    return created_user


@router.patch("/verify", response_model=UserResponse)
def verify_user_account(request_data: VerifyOTPRequest):

    verified_user = verify_user(request_data.otp)

    return verified_user


@router.patch("/resend-otp", response_model=UserResponse)
def resend_otp(request_data: ResendOtpRequest):

    user = generate_new_otp(request_data.email)

    return user

@router.get("/me", response_model=UserResponse)
def get_current_user(user_id: str = Depends(get_current_user_id)):

    user = get_user_by_id(user_id)

    return user