from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, description="使用者名稱不得為空")
    password: str = Field(..., min_length=1, description="密碼不得為空")


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=4, description="使用者名稱不得為空")
    password: str = Field(..., min_length=4, description="密碼不得為空")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
