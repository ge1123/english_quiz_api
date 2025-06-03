from fastapi import FastAPI, HTTPException, Query, Body
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from pydantic import BaseModel
import pyodbc
import random


# ----------------------
# 資料結構定義
# ----------------------
class WordItem(BaseModel):
    EnglishWord: str
    ChineseMeaning: str
    Level: int


class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    isAnswerIncluded: bool
    correct: str
    level: int  # ✅ 新增這行


class QuizRequest(BaseModel):
    level: Optional[List[int]] = []
    area: Optional[List[int]] = []


# ----------------------
# FastAPI App 初始化
# ----------------------
app = FastAPI(title="Word Quiz API")

# 開啟跨來源支援（前後端不同埠需要）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生產環境請設定白名單
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------
# 資料庫連線
# ----------------------
CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=172.28.167.25,1761;"
    "DATABASE=EnglishQuiz;"
    "UID=sa;"
    "PWD=P@55word;"
)


def get_db_connection():
    try:
        return pyodbc.connect(CONN_STR, autocommit=True)
    except Exception as e:
        raise RuntimeError(f"資料庫連線失敗: {e}")


# ----------------------
# Endpoint: 所有單字
# ----------------------
@app.get("/api/words", response_model=List[WordItem])
def get_words(level: Optional[int] = None):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        if level is not None:
            cursor.execute(
                "SELECT EnglishWord, ChineseMeaning, Level FROM WordList WHERE Level = ?",
                level,
            )
        else:
            cursor.execute("SELECT EnglishWord, ChineseMeaning, Level FROM WordList")
        rows = cursor.fetchall()
        return [
            WordItem(
                EnglishWord=row.EnglishWord,
                ChineseMeaning=row.ChineseMeaning,
                Level=row.Level,
            )
            for row in rows
        ]
    finally:
        cursor.close()
        conn.close()


# ----------------------
# Endpoint: 隨機單字
# ----------------------
@app.post("/api/words/random", response_model=QuizQuestion)
def get_random_question(payload: QuizRequest = Body(...)):
    level = payload.level or []
    area = payload.area or []

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 撈資料（根據 level 過濾）
        if level:
            placeholders = ",".join(["?"] * len(level))
            sql = f"SELECT EnglishWord, ChineseMeaning, Level FROM WordList WHERE Level IN ({placeholders})"
            cursor.execute(sql, level)
        else:
            cursor.execute("SELECT EnglishWord, ChineseMeaning, Level FROM WordList")

        rows = cursor.fetchall()
        if len(rows) < 10:
            raise HTTPException(status_code=400, detail="資料不足")

        # 分區 area 處理
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

        # 隨機正解
        correct = random.choice(rows)
        correct_en = correct.EnglishWord
        correct_zh = correct.ChineseMeaning
        correct_level = correct.Level  # ✅ 新增這行

        include_answer = random.random() > 0.3

        # 建立選項
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
            level=correct_level,  # ✅ 回傳 level
        )

    finally:
        cursor.close()
        conn.close()


# ----------------------
# Endpoint: 儲存正確回答（模擬）
# ----------------------
@app.get("/save-correct")
def save_correct(word: str = Query(..., description="正確的英文單字")):
    print(f"✅ 使用者答對了：{word}")  # 日誌輸出，可改成寫檔或寫 DB
    return {"message": "紀錄成功", "word": word}
