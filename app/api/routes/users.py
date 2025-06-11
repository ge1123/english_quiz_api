from fastapi import APIRouter, Depends
from app.dependencies.service_provider import get_auth_service
from app.services.auth_service import AuthService
from app.schemas.user import LoginRequest, RegisterRequest, TokenResponse

router = APIRouter()


@router.post("/login", response_model=TokenResponse)
async def login(
        data: LoginRequest,
        auth_service: AuthService = Depends(get_auth_service)
) -> TokenResponse:
    token, user_id = await auth_service.login(data.username, data.password)
    return TokenResponse(
        access_token=token,
        user_id=user_id
    )


@router.post("/register", status_code=201)
async def register_user(
        data: RegisterRequest,
        auth_service: AuthService = Depends(get_auth_service)
) -> dict[str, str | int]:
    user_id = await auth_service.register(data)
    return {"msg": "User registered successfully", "user_id": user_id}
