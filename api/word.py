from fastapi import APIRouter, Depends, HTTPException, Query, Body
from typing import List, Optional
from models.schema import (
    WordItem,
    QuizRequest,
    QuizQuestion,
    QuizCorrectRequest)
from services.word_service import (
    get_words_by_level,
    get_random_question,
    get_word_bank,
    log_correct_answer)
from sqlalchemy.ext.asyncio import AsyncSession
from db.async_connection import get_async_session
from services.auth import get_current_user

router = APIRouter()


@router.get("", response_model=List[WordItem])
async def get_words(
        level: Optional[int] = None,
        session: AsyncSession = Depends(get_async_session),
) -> list[WordItem]:
    return await get_words_by_level(level, session)


@router.post("/random", response_model=QuizQuestion)
async def random_quiz(
        payload: QuizRequest = Body(...),
        session: AsyncSession = Depends(get_async_session),
        current_user: str = Depends(get_current_user),  # ✅ 這行會強制驗證
) -> QuizQuestion:
    return await get_random_question(payload, session)


@router.post("/bank", response_model=list[WordItem])
async def word_bank(
        payload: QuizRequest = Body(...),
        session: AsyncSession = Depends(get_async_session),
        current_user: str = Depends(get_current_user),  # ✅ 這行會強制驗證
) -> list[dict]:
    return await get_word_bank(payload, session)


@router.post("/save-correct")
async def save_correct_answer(
        payload: QuizCorrectRequest = Body(...),
        session: AsyncSession = Depends(get_async_session),
) -> None:
    return await log_correct_answer(payload.wordId, payload.userId, session)
