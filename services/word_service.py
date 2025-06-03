from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from models.schema import WordItem, QuizRequest, QuizQuestion
from models.schema import WordList
from fastapi import HTTPException
import random


async def get_words_by_level(level: int, session: AsyncSession):
    try:
        stmt = select(WordList)
        if level is not None:
            stmt = stmt.where(WordList.Level == level)

        result = await session.execute(stmt)
        rows = result.scalars().all()

        return [
            WordItem(
                EnglishWord=row.EnglishWord,
                ChineseMeaning=row.ChineseMeaning,
                Level=row.Level,
            )
            for row in rows
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"讀取單字失敗: {e}")


async def get_random_question(
    payload: QuizRequest, session: AsyncSession
) -> QuizQuestion:
    level = payload.level or []
    area = payload.area or []

    try:
        stmt = select(WordList)
        if level:
            stmt = stmt.where(WordList.Level.in_(level))

        result = await session.execute(stmt)
        rows = result.scalars().all()

        if len(rows) < 10:
            raise HTTPException(status_code=400, detail="資料不足")

        if area:
            total_rows = len(rows)
            rows_per_area = total_rows // 10
            chunks = [
                rows[i * rows_per_area : (i + 1) * rows_per_area] for i in range(10)
            ]

            filtered_rows = []
            for a in area:
                index = a - 1
                if 0 <= index < len(chunks):
                    filtered_rows.extend(chunks[index])

            if len(filtered_rows) < 10:
                raise HTTPException(status_code=400, detail="符合 area 條件的資料不足")
            rows = filtered_rows

        correct = random.choice(rows)
        correct_en = correct.EnglishWord
        correct_zh = correct.ChineseMeaning
        correct_level = correct.Level

        include_answer = random.random() > 0.3

        choices = set()
        while len(choices) < 10:
            ch = random.choice(rows).ChineseMeaning
            if ch != correct_zh:
                choices.add(ch)

        choices = list(choices)
        if include_answer:
            insert_index = random.randint(0, 9)
            choices[insert_index] = correct_zh

        random.shuffle(choices)

        return QuizQuestion(
            question=correct_en,
            options=choices,
            isAnswerIncluded=include_answer,
            correct=correct_zh,
            level=correct_level,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"題目生成失敗: {e}")
