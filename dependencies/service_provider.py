from fastapi import Depends
from db.async_connection import get_async_session
from services.auth_service import AuthService
from services.word_service import WordService


def get_auth_service(session=Depends(get_async_session)) -> AuthService:
    return AuthService(session)


def get_word_service(session=Depends(get_async_session)) -> WordService:
    return WordService(session)
