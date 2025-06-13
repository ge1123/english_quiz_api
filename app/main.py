from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import router
from app.middleware.cors import add_cors
from app.middleware.logging import log_requests
from app.core.logging_config import setup_logger
setup_logger()

app = FastAPI(title="English Quiz API")

# 開啟 CORS，允許前端跨域請求
add_cors(app)
# 加入日誌中介層
app.middleware("http")(log_requests)

# 掛載路由
app.include_router(router)
