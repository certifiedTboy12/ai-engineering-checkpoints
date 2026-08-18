from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    first_name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    last_name: str = Field(
        ...,
        min_length=2,
        max_length=100
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        max_length=128
    )

    otp: str | None = Field(
        default=None,
        min_length=6,
        max_length=6
    )

    otp_expiry: datetime | None = None


class UserUpdate(BaseModel):
    first_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    last_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    email: EmailStr | None = None

    password: str | None = Field(
        default=None,
        min_length=8,
        max_length=128
    )

    otp: str | None = Field(
        default=None,
        min_length=6,
        max_length=6
    )

    otp_expiry: datetime | None = None


class VerifyOTPRequest(BaseModel):
    otp: str = Field(
        ...,
        min_length=6,
        max_length=6
    )

class ResendOtpRequest(BaseModel):
    email: EmailStr

class UserResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: EmailStr
    otp: str | None
    otp_expiry: datetime | None
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)