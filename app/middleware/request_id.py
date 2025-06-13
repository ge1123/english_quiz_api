import uuid
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.requests import Request


class RequestIDMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            # 非 HTTP 請求（例如 WebSocket），直接略過
            await self.app(scope, receive, send)
            return

        # 儲存 request_id 到 scope["state"]
        request = Request(scope)
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        request.state.request_id = request_id  # ✅ 這是關鍵改法！

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                headers = message.setdefault("headers", [])
                headers.append((b"x-request-id", request_id.encode()))
            await send(message)

        await self.app(scope, receive, send_wrapper)
