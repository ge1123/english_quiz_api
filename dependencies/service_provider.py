from fastapi import Depends
from repositories.word_repository import WordRepository
from services.auth_service import AuthService
from services.word_service import WordService
from repositories.user_repository import UserRepository
from dependencies.repository_provider import get_user_repository, get_word_repository


def get_auth_service(user_repo: UserRepository = Depends(get_user_repository)) -> AuthService:
    return AuthService(user_repo)


def get_word_service(word_repo: WordRepository = Depends(get_word_repository)) -> WordService:
    return WordService(word_repo)
