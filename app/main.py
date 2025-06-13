from fastapi import FastAPI
from app.api.routes import router
from app.middleware.cors import add_cors
from app.middleware.logging import LoggingMiddleware
from app.middleware.request_id import RequestIDMiddleware
from app.core.logging_config import setup_logger

# 初始化 logger
setup_logger()

# 建立 FastAPI 應用
app = FastAPI(title="English Quiz API")

# 註冊 middleware
# app.add_middleware(RequestIDMiddleware)   # 產生 request_id 並掛入 request.state
add_cors(app)                              # 開啟 CORS 支援
# app.add_middleware(LoggingMiddleware)

# 掛載路由
app.include_router(router)
