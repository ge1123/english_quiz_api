from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import word
from api import users

app = FastAPI(title="English Quiz API (Async)")

# 開啟 CORS，允許前端跨域請求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生產環境建議改為特定網域
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 掛載路由
app.include_router(word.router, prefix="/api/words", tags=["Word Quiz"])
app.include_router(users.router, prefix="/api/users", tags=["User Auth"])
# app.include_router(users.router, prefix="/api/register", tags=["User Auth"])
