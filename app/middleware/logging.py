from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.requests import Request
from starlette.responses import Response
from loguru import logger
import time

class LoggingMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive)
        start = time.time()
        request_id = getattr(request.state, "request_id", "MISSING")

        try:
            if request.headers.get("content-type", "").startswith("application/json"):
                body = await request.json()
            else:
                body = None
        except Exception:
            body = None

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                duration = round(time.time() - start, 4)
                log_data = {
                    "request_id": request_id,
                    "method": request.method,
                    "url": str(request.url),
                    "status": message.get("status", 0),
                    "duration": f"{duration}s",
                    "content_type": request.headers.get("content-type", ""),
                }

                if body:
                    logger.bind(request_id=request_id).debug(f"Request body: {body}")

                if log_data["status"] >= 500:
                    logger.bind(request_id=request_id).error(f"Server Error: {log_data}")
                elif log_data["status"] >= 400:
                    logger.bind(request_id=request_id).warning(f"Client Error: {log_data}")
                else:
                    logger.bind(request_id=request_id).info(f"Request Info: {log_data}")

            await send(message)

        await self.app(scope, receive, send_wrapper)
