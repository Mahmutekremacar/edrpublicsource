from abc import ABC, abstractmethod
from typing import Optional
from schemas.logs import PolymorphicLogEvent

class BaseDetector(ABC):
    @abstractmethod
    def analyze(self, event: PolymorphicLogEvent) -> Optional[str]:
        """Analyze the event and return an alert string if malicious, else None."""
        pass

class DummyAnomalyDetector(BaseDetector):
    def analyze(self, event: PolymorphicLogEvent) -> Optional[str]:
        if event.event_type == "network":
            if str(event.dest_port) == "4444":
                return f"Windows Alert: Suspicious network traffic to port 4444 from {event.source_ip}"
        
        elif event.event_type == "sysmon":
            # Sysmon EventId 3 -> Network Connection
            if str(event.event_id) == "3" and event.EventData:
                dest_port = event.EventData.get("DestinationPort")
                if str(dest_port) == "4444":
                    return "Sysmon Alert: Port 4444"
        
        return None