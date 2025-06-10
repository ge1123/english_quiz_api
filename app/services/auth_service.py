from app.models import User
from datetime import timedelta
from fastapi import HTTPException, status
from app.schemas.user import RegisterRequest
from app.utils.security import hash_password, verify_password
from app.utils.jwt_helper import create_access_token
from app.repositories.user_repository import UserRepository

ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def login(self, username: str, password: str) -> tuple[str, int]:
        user = await self.user_repo.get_by_username(username)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
            )

        token = create_access_token(
            data={"sub": user.username},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )
        return token, user.id

    async def register(self, data: RegisterRequest) -> int:
        existing_user = await self.user_repo.get_by_username(data.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )

        new_user = User(
            username=data.username,
            hashed_password=hash_password(data.password)
        )
        user = await self.user_repo.add(new_user)
        return user.id
