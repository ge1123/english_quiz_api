from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.user import User, RegisterRequest
from utils.security import hash_password, verify_password
from utils.jwt_helper import create_access_token

ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def login(self, username: str, password: str) -> tuple[str, int]:
        stmt = select(User).where(User.username == username)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

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
        stmt = select(User).where(User.username == data.username)
        result = await self.session.execute(stmt)
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered",
            )

        new_user = User(
            username=data.username,
            hashed_password=hash_password(data.password)
        )

        self.session.add(new_user)
        await self.session.commit()
        await self.session.refresh(new_user)

        return new_user.id
