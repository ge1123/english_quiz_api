from fastapi import Depends
from db.async_connection import get_async_session
from repositories.user_repository import UserRepository
from repositories.word_repository import WordRepository


def get_user_repository(session=Depends(get_async_session)) -> UserRepository:
    return UserRepository(session)

def get_word_repository(session=Depends(get_async_session)) -> WordRepository:
    return WordRepository(session)
