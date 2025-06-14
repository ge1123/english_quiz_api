from pydantic import BaseModel
from typing import List, Optional


class QuizRequest(BaseModel):
    level: Optional[List[int]] = []
    area: Optional[List[int]] = []


class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    isAnswerIncluded: bool
    correct: str
    level: int
    wordId: int


class QuizCorrectRequest(BaseModel):
    wordId: int
    userId: int


class WordItem(BaseModel):
    EnglishWord: str
    ChineseMeaning: str
    Level: int
