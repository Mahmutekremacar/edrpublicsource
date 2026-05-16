from fastapi import APIRouter, HTTPException, Depends
from schemas.logs import ClientRegistration, IngestBatchRequest
from services.client_service import ClientService
from services.ingestion_service import IngestionService
from core.dependencies import get_client_service, get_ingestion_service

router = APIRouter(tags=["clients"])

@router.post("/clients/register")
def register_client(payload: ClientRegistration, clients: ClientService = Depends(get_client_service)):
    return clients.register_client(payload)

@router.get("/clients")
def list_clients(clients: ClientService = Depends(get_client_service)):
    return clients.list_clients()

@router.get("/stats")
def stats(clients: ClientService = Depends(get_client_service)):
    return clients.get_global_stats()

@router.get("/ingest/{client_id}/last")
def last_ingest_result(client_id: str, ingestion: IngestionService = Depends(get_ingestion_service)):
    result = ingestion.last_result(client_id)
    if result is None:
        raise HTTPException(status_code=404, detail="No ingest result for this client")
    return result