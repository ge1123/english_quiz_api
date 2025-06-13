from starlette.requests import Request
from starlette.responses import Response
from loguru import logger
import time


async def log_requests(request: Request, call_next):
    start = time.time()

    # 嘗試讀取 Request body（限 JSON，避免洩露敏感資料）
    body = None
    try:
        if request.headers.get("content-type", "").startswith("application/json"):
            body = await request.json()
    except Exception:
        body = None

    # 執行主邏輯，取得 Response
    response: Response = await call_next(request)
    duration = round(time.time() - start, 4)

    # 基本 meta 資訊
    log_data = {
        "method": request.method,
        "url": str(request.url),
        "status": response.status_code,
        "duration": f"{duration}s",
        "content_type": response.headers.get("content-type", ""),
    }

    # 若是 DEBUG 等級，顯示 request body
    if body is not None:
        logger.debug(f"Request body: {body}")

    # 根據 status 決定 log 等級
    if response.status_code >= 500:
        logger.error(f"Server Error: {log_data}")
    elif response.status_code >= 400:
        logger.warning(f"Client Error: {log_data}")
    else:
        logger.info(f"Request Info: {log_data}")

    return response
