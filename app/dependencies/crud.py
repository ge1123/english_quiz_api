from fastapi import Depends
from app.dependencies.db import get_db
from app.crud.user import UserRepository
from app.crud.word import WordRepository


def get_user_repository(session=Depends(get_db)) -> UserRepository:
    return UserRepository(session)

def get_word_repository(session=Depends(get_db)) -> WordRepository:
    return WordRepository(session)
