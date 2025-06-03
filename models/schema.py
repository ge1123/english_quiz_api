from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


# SQLAlchemy ORM Model
class WordList(Base):
    __tablename__ = "WordList"

    Id = Column(Integer, primary_key=True, index=True)
    EnglishWord = Column(String)
    ChineseMeaning = Column(String)
    Level = Column(Integer)


class WordItem(BaseModel):
    EnglishWord: str
    ChineseMeaning: str
    Level: int


class QuizRequest(BaseModel):
    level: Optional[List[int]] = []
    area: Optional[List[int]] = []


class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    isAnswerIncluded: bool
    correct: str
    level: int
