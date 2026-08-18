from pydantic import BaseModel, ConfigDict, EmailStr


class UserLogin(BaseModel):
    email: EmailStr
    password: str 

   
class AuthResponse(BaseModel):
    access_token: str
    model_config = ConfigDict(from_attributes=True)