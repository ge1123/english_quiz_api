from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


# SQLAlchemy ORM Model
class WordList(Base):
    __tablename__ = "WordList"

    Id = Column(Integer, primary_key=True, index=True)
    EnglishWord = Column(String)
    ChineseMeaning = Column(String)
    Level = Column(Integer)


class WordCorrectLog(Base):
    __tablename__ = "WordCorrectLog"

    Id = Column(Integer, primary_key=True, index=True)
    WordId = Column(Integer, ForeignKey("WordList.Id"), nullable=False)
    UserId = Column(Integer, nullable=True)
    AnsweredAt = Column(DateTime, server_default=func.getdate(), nullable=False)


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


class QuizCorrectRequest(BaseModel):
    wordId: int = []
    userId: int = []
