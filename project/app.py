import logging

from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from fastapi_simple_security import api_key_router

from project import CONFIG

logging.basicConfig(
    format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

title = CONFIG.get("app", "title")
description = CONFIG.get("app", "description")

app = FastAPI(
    title=title,
    description="description",
)

app.include_router(api_key_router, prefix="/auth", tags=["_auth"])


@app.get("/health", response_class=PlainTextResponse)
def healthcheck() -> str:
    """Healthcheck, for use in automatic ."""
    return "200"
