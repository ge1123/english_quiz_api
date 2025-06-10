from fastapi import Depends
from db.async_connection import get_async_session
from services.auth_service import AuthService

def get_auth_service(session=Depends(get_async_session)) -> AuthService:
    return AuthService(session)
