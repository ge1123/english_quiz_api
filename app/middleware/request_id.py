import uuid
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.requests import Request

class RequestIDMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # ✅ 正確設定方式：直接設定 scope["state"]
        request_id = scope.get("headers", [])
        request_id = dict(request_id).get(b'x-request-id', str(uuid.uuid4()).encode()).decode()

        scope.setdefault("state", {})["request_id"] = request_id

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                headers = message.setdefault("headers", [])
                headers.append((b"x-request-id", request_id.encode()))
            await send(message)

        await self.app(scope, receive, send_wrapper)
