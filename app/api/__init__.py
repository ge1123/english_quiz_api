# app/api/routes/__init__.py
from fastapi import APIRouter
from app.api.routes.users import router as user_router
from app.api.routes.word import router as word_router

router = APIRouter()
router.include_router(user_router, prefix="/api/users", tags=["User Auth"])
router.include_router(word_router, prefix="/api/words", tags=["Word Quiz"])
