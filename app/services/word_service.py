from app.schemas.word import (
    WordItem,
    QuizRequest,
    QuizQuestion,
)
from fastapi import HTTPException
import random
from app.repositories.word_repository import WordRepository


class WordService:
    def __init__(self, word_repo: WordRepository):
        self.word_repo = word_repo

    def _split_rows_by_area(self, rows: list, area: list[int], group_count: int) -> list:
        total_rows = len(rows)
        rows_per_area = total_rows // group_count
        chunks = [
            rows[i * rows_per_area: (i + 1) * rows_per_area]
            for i in range(group_count - 1)
        ]
        chunks.append(rows[(group_count - 1) * rows_per_area:])

        filtered_rows = []
        for a in area:
            index = a - 1
            if 0 <= index < len(chunks):
                filtered_rows.extend(chunks[index])
        return filtered_rows

    async def get_words_by_level(self, level: int) -> list[WordItem]:
        try:
            rows = await self.word_repo.get_by_levels([level])
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

    async def get_random_question(self, payload: QuizRequest, area_group_count: int = 10) -> QuizQuestion:
        try:
            rows = await self.word_repo.get_by_levels(payload.level or [])
            if len(rows) < 10:
                raise HTTPException(status_code=400, detail="資料不足")

            if payload.area:
                rows = self._split_rows_by_area(rows, payload.area, area_group_count)
                if len(rows) < 10:
                    raise HTTPException(status_code=400, detail="符合 area 條件的資料不足")

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

    async def get_word_bank(self, payload: QuizRequest, area_group_count: int = 30) -> list[dict]:
        try:
            rows = await self.word_repo.get_by_levels(payload.level or [1])
            if not rows:
                raise HTTPException(status_code=400, detail="查無資料")

            if payload.area:
                rows = self._split_rows_by_area(rows, payload.area, area_group_count)
                if not rows:
                    raise HTTPException(status_code=400, detail="符合 area 條件的資料不足")

            return [
                {
                    "EnglishWord": row.EnglishWord,
                    "ChineseMeaning": row.ChineseMeaning,
                    "Level": row.Level,
                }
                for row in rows
            ]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"題庫取得失敗: {e}")

    async def log_correct_answer(self, word_id: int, user_id: int | None):
        try:
            await self.word_repo.log_correct_answer(word_id, user_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"記錄答對失敗: {e}")
