from fastapi import Depends
from app.db.async_connection import get_async_session
from app.repositories.user_repository import UserRepository
from app.repositories.word_repository import WordRepository


def get_user_repository(session=Depends(get_async_session)) -> UserRepository:
    return UserRepository(session)

def get_word_repository(session=Depends(get_async_session)) -> WordRepository:
    return WordRepository(session)
