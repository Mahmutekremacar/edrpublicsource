from fastapi import APIRouter
from api import clients, ingest

api_router = APIRouter(prefix="/api")
#api_router.include_router(health.router)
#api_router.include_router(metadata.router)
api_router.include_router(clients.router)
api_router.include_router(ingest.router)