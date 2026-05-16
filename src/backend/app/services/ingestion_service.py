from typing import Dict, Optional
from threading import Lock
from schemas.logs import IngestBatchRequest, PipelineSummary
from services.client_service import ClientService
from services.pipeline_service import DummyPipeline

class IngestionService:
    def __init__(self, client_service: ClientService, pipeline: DummyPipeline):
        self.client_service = client_service
        self.pipeline = pipeline
        self._last_results: Dict[str, PipelineSummary] = {}
        self._lock = Lock()

    def ingest(self, client_id: str, request: IngestBatchRequest, hostname: str | None) -> PipelineSummary:
        self.client_service.get_or_create_client(client_id, hostname)
        self.client_service.update_client_stats(client_id, len(request.messages))

        source = f"{request.source}:{client_id}"
        result_dict = self.pipeline.process_batch(request.messages, source=source)
        result = PipelineSummary(**result_dict)

        with self._lock:
            self._last_results[client_id] = result
        return result

    def last_result(self, client_id: str) -> Optional[PipelineSummary]:
        with self._lock:
            return self._last_results.get(client_id)