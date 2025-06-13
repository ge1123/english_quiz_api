from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.requests import Request
from loguru import logger
import time
import json


class LoggingMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        body_bytes = b""
        more_body = True

        # 🧠 收集完整 body
        async def receive_body():
            nonlocal body_bytes, more_body
            while more_body:
                message = await receive()
                if message["type"] == "http.request":
                    body_bytes += message.get("body", b"")
                    more_body = message.get("more_body", False)

        await receive_body()

        # 🧠 用來餵回原本的 body 給 FastAPI
        async def receive_wrapper():
            return {"type": "http.request", "body": body_bytes, "more_body": False}

        request = Request(scope, receive_wrapper)
        start = time.time()
        request_id = getattr(request.state, "request_id", "MISSING")

        # 🧠 解析 JSON body
        try:
            content_type = request.headers.get("content-type", "").lower()
            if content_type.startswith("application/json"):
                body = json.loads(body_bytes.decode("utf-8"))
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

        await self.app(scope, receive_wrapper, send_wrapper)
