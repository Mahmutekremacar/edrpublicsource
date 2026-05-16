from pydantic import BaseModel, Field
from typing import Literal, Union, Dict, Any, Optional, List
from typing_extensions import Annotated


class ClientRegistration(BaseModel):
    client_id: str
    hostname: Optional[str] = None
    environment: Optional[str] = None
    description: Optional[str] = None

class ClientStats(BaseModel):
    client_id: str
    hostname: Optional[str] = None
    environment: Optional[str] = None
    description: Optional[str] = None
    logs_received: int = 0
    batches_received: int = 0
    last_seen: Optional[str] = None

class PipelineSummary(BaseModel):
    status: str = "received"
    message_count: int
    alerts_triggered: int = 0
    event_type_counts: Dict[str, int] = {}
    source: Optional[str] = None



class NetworkLog(BaseModel):
    event_type: Literal["network"]
    source_ip: str
    dest_ip: str
    source_port: int
    dest_port: int
    protocol: str

class SysmonLog(BaseModel):
    event_type: Literal["sysmon"]
    record_id: Optional[int] = None
    event_id: Optional[str] = None
    timestamp: Optional[str] = None
    EventData: Optional[Dict[str, Any]] = None

PolymorphicLogEvent = Annotated[
    Union[NetworkLog, SysmonLog], 
    Field(discriminator="event_type")
]


class IngestBatchRequest(BaseModel):
    source: str = "unknown"
    messages: List[PolymorphicLogEvent]