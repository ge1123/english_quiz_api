from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import WordList, WordCorrectLog


class WordRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_levels(self, levels: list[int]) -> list[WordList]:
        stmt = select(WordList)
        if levels:
            stmt = stmt.where(WordList.Level.in_(levels))
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_all(self) -> list[WordList]:
        result = await self.session.execute(select(WordList))
        return result.scalars().all()

    async def log_correct_answer(self, word_id: int, user_id: int | None):
        log = WordCorrectLog(WordId=word_id, UserId=user_id)
        self.session.add(log)
        await self.session.commit()
