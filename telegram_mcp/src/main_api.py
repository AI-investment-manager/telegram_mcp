from fastapi import APIRouter, FastAPI

from src.adapter.inbound.web.routes.health import router as health_router
from src.adapter.inbound.web.routes.message import router as message_router
from src.infrastructure.container import Container

container = Container()

app = FastAPI(title="Telegram MCP Server", version="0.1.0")
app.container = container

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(health_router)
api_v1_router.include_router(message_router)

app.include_router(api_v1_router)
