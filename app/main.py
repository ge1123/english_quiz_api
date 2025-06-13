from fastapi import FastAPI
from app.api.routes import router
from app.middleware.cors import add_cors
from app.middleware.logging import LoggingMiddleware
from app.middleware.request_id import RequestIDMiddleware
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.logging_config import setup_logger
from app.exceptions.handlers import (
    http_exception_handler,
    validation_exception_handler,
    global_exception_handler,
)

# 初始化 logger
setup_logger()

# 建立 FastAPI 應用
app = FastAPI(title="English Quiz API")


# 註冊 middleware
add_cors(app)  # 開啟 CORS 支援
app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestIDMiddleware)   # 產生 request_id 並掛入 request.state

app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

# 掛載路由
app.include_router(router)
