import logging
from typing import List
from schemas.logs import PolymorphicLogEvent
from detection.rules import DummyAnomalyDetector

logger = logging.getLogger("EDR_Central")

class DummyPipeline:
    def __init__(self):
        self.detectors = [DummyAnomalyDetector()]

    def process_batch(self, messages: List[PolymorphicLogEvent], source=None) -> dict:
        alerts_triggered = 0
        event_counts = {}

        for msg in messages:
            event_counts[msg.event_type] = event_counts.get(msg.event_type, 0) + 1
            for detector in self.detectors:
                alert = detector.analyze(msg)
                if alert:
                    logger.warning(f"🚨 Source: {source} - {alert}")
                    print(f"🚨 ALERT DETECTED: {alert}")
                    alerts_triggered += 1

        return {
            "status": "processed",
            "message_count": len(messages),
            "alerts_triggered": alerts_triggered,
            "event_type_counts": event_counts,
            "source": source
        }