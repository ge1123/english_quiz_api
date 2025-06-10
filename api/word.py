from fastapi import APIRouter, Depends, Body
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from db.async_connection import get_async_session
from dependencies.service_provider import get_word_service
from dependencies.auth_guard import get_current_user
from services.word_service import WordService
from schemas.word import QuizCorrectRequest, QuizRequest, QuizQuestion, WordItem

router = APIRouter()


@router.get("", response_model=List[WordItem])
async def get_words(
        level: Optional[int] = None,
        session: AsyncSession = Depends(get_async_session),
        word_service: WordService = Depends(get_word_service)

) -> list[WordItem]:
    return await word_service.get_words_by_level(level, session)


@router.post("/random", response_model=QuizQuestion)
async def random_quiz(
        payload: QuizRequest = Body(...),
        session: AsyncSession = Depends(get_async_session),
        current_user: str = Depends(get_current_user),  # ✅ 這行會強制驗證
        word_service: WordService = Depends(get_word_service)
) -> QuizQuestion:
    return await word_service.get_random_question(payload, session)


@router.post("/bank", response_model=list[WordItem])
async def word_bank(
        payload: QuizRequest = Body(...),
        session: AsyncSession = Depends(get_async_session),
        current_user: str = Depends(get_current_user),  # ✅ 這行會強制驗證
        word_service: WordService = Depends(get_word_service)
) -> list[dict]:
    return await word_service.get_word_bank(payload, session)


@router.post("/save-correct")
async def save_correct_answer(
        payload: QuizCorrectRequest = Body(...),
        session: AsyncSession = Depends(get_async_session),
        word_service: WordService = Depends(get_word_service)
) -> None:
    return await word_service.log_correct_answer(payload.wordId, payload.userId, session)
