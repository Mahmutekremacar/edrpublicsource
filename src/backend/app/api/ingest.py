from fastapi import APIRouter, Depends
from schemas.logs import IngestBatchRequest
from services.ingestion_service import IngestionService
from core.dependencies import get_ingestion_service

router = APIRouter(tags=["ingest"])

@router.post("/ingest/json/{client_id}")
def ingest_json_logs(
    client_id: str, 
    payload: IngestBatchRequest, 
    hostname: str | None = None,
    ingestion: IngestionService = Depends(get_ingestion_service)
):
    return ingestion.ingest(client_id, payload, hostname)