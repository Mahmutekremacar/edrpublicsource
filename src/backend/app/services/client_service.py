from datetime import datetime, timezone
from threading import Lock
from typing import Dict, List
from schemas.logs import ClientRegistration, ClientStats

class ClientService:
    def __init__(self):
        self._clients: Dict[str, ClientStats] = {}
        self._lock = Lock()

    def register_client(self, registration: ClientRegistration) -> ClientStats:
        with self._lock:
            existing = self._clients.get(registration.client_id)
            if existing:
                existing.hostname = registration.hostname or existing.hostname
                existing.environment = registration.environment or existing.environment
                existing.description = registration.description or existing.description
                return existing

            stats = ClientStats(
                client_id=registration.client_id,
                hostname=registration.hostname,
                environment=registration.environment,
                description=registration.description,
            )
            self._clients[registration.client_id] = stats
            return stats

    def get_or_create_client(self, client_id: str, hostname: str | None = None) -> ClientStats:
        with self._lock:
            stats = self._clients.get(client_id)
            if not stats:
                stats = ClientStats(client_id=client_id, description="auto-registered")
                self._clients[client_id] = stats
            if hostname:
                stats.hostname = hostname
            return stats

    def update_client_stats(self, client_id: str, log_count: int):
        with self._lock:
            stats = self._clients.get(client_id)
            if stats:
                stats.batches_received += 1
                stats.logs_received += log_count
                stats.last_seen = datetime.now(timezone.utc).isoformat()

    def list_clients(self) -> List[ClientStats]:
        with self._lock:
            return list(self._clients.values())

    def get_global_stats(self) -> dict:
        with self._lock:
            total_logs = sum(client.logs_received for client in self._clients.values())
            total_batches = sum(client.batches_received for client in self._clients.values())
            return {
                "registered_clients": len(self._clients),
                "total_batches_received": total_batches,
                "total_logs_received": total_logs,
                "clients": list(self._clients.values()),
            }