from services.client_service import ClientService
from services.pipeline_service import DummyPipeline
from services.ingestion_service import IngestionService

_client_service = ClientService()
_pipeline_service = DummyPipeline()
_ingestion_service = IngestionService(client_service=_client_service, pipeline=_pipeline_service)

def get_client_service() -> ClientService:
    return _client_service

def get_ingestion_service() -> IngestionService:
    return _ingestion_service