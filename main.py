import os
import time
import uuid
from typing import Callable, Awaitable

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from starlette.types import ASGIApp, Scope, Receive, Send, Message

EMAIL = "24f1002110@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-n1d87a.example.com"


class RequestMetricsMiddleware:
    """Adds request ID and processing time to every response, including CORS preflights."""

    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request_id = str(uuid.uuid4())
        start = time.perf_counter()

        async def send_with_metrics(message: Message) -> None:
            if message["type"] == "http.response.start":
                elapsed = max(0.0, time.perf_counter() - start)
                headers = list(message.get("headers", []))
                headers.extend([
                    (b"x-request-id", request_id.encode("ascii")),
                    (b"x-process-time", f"{elapsed:.6f}".encode("ascii")),
                ])
                message["headers"] = headers
            await send(message)

        await self.app(scope, receive, send_with_metrics)


api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@api.get("/stats")
async def stats(values: str = Query(..., description="Comma-separated integers")):
    try:
        numbers = [int(item.strip()) for item in values.split(",")]
        if not numbers or any(item == "" for item in values.split(",")):
            raise ValueError("empty integer")
    except (ValueError, AttributeError):
        raise HTTPException(status_code=400, detail="values must be comma-separated integers")

    total = sum(numbers)
    return {
        "email": EMAIL,
        "count": len(numbers),
        "sum": total,
        "min": min(numbers),
        "max": max(numbers),
        "mean": total / len(numbers),
    }


# Wrap outside CORSMiddleware so even preflight/rejected responses get required headers.
app = RequestMetricsMiddleware(api)
