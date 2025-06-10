from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.sql import func
from .base import Base


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
