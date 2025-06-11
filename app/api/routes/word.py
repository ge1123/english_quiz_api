from fastapi import APIRouter, Depends, Body
from typing import List, Optional
from app.dependencies.services import get_word_service
from app.services.word import WordService
from app.schemas.word import QuizCorrectRequest, QuizRequest, QuizQuestion, WordItem
from app.api.deps import get_current_user

router = APIRouter()


@router.get("", response_model=List[WordItem])
async def get_words(
        level: Optional[int] = None,
        word_service: WordService = Depends(get_word_service)

) -> list[WordItem]:
    return await word_service.get_words_by_level(level)


@router.post("/random", response_model=QuizQuestion)
async def random_quiz(
        payload: QuizRequest = Body(...),
        current_user: str = Depends(get_current_user),  # ✅ 這行會強制驗證
        word_service: WordService = Depends(get_word_service)
) -> QuizQuestion:
    return await word_service.get_random_question(payload)


@router.post("/bank", response_model=list[WordItem])
async def word_bank(
        payload: QuizRequest = Body(...),
        current_user: str = Depends(get_current_user),  # ✅ 這行會強制驗證
        word_service: WordService = Depends(get_word_service)
) -> list[dict]:
    return await word_service.get_word_bank(payload)


@router.post("/save-correct")
async def save_correct_answer(
        payload: QuizCorrectRequest = Body(...),
        word_service: WordService = Depends(get_word_service)
) -> None:
    return await word_service.log_correct_answer(payload.wordId, payload.userId, session)
