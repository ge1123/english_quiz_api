from fastapi import APIRouter, Depends, HTTPException, Query, Body
from typing import List, Optional
from models.schema import WordItem, QuizRequest, QuizQuestion
from services.word_service import get_words_by_level, get_random_question
from sqlalchemy.ext.asyncio import AsyncSession
from db.async_connection import get_async_session
from services.auth import get_current_user

router = APIRouter()


@router.get("", response_model=List[WordItem])
async def get_words(
    level: Optional[int] = None,
    session: AsyncSession = Depends(get_async_session),
):
    return await get_words_by_level(level, session)


@router.post("/random", response_model=QuizQuestion)
async def random_quiz(
    payload: QuizRequest = Body(...),
    session: AsyncSession = Depends(get_async_session),
    current_user: str = Depends(get_current_user),  # ✅ 這行會強制驗證
):
    return await get_random_question(payload, session)


@router.get("/save-correct")
def save_correct(word: str = Query(...)):
    print(f"✅ 答對：{word}")
    return {"message": "紀錄成功", "word": word}
