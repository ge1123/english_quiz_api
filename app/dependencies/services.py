from fastapi import Depends
from app.crud.word import WordRepository
from app.services.user import AuthService
from app.services.word import WordService
from app.crud.user import UserRepository
from app.dependencies.crud import get_user_repository, get_word_repository


def get_auth_service(user_repo: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repo)


def get_word_service(word_repo: WordRepository = Depends(get_word_repository)) -> WordService:
    return WordService(word_repo)
