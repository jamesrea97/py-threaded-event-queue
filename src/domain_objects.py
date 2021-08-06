"""Module contains domain objects"""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4


class Status(Enum):
    NOT_FOUND = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"


@dataclass
class DbResponse:
    event_id: uuid4
    request: str
    status: Status
    data: Optional[str]
    timestamp: datetime = datetime.now()

    def to_json(self):
        return {
            "datetime": str(self.timestamp),
            "event_id": str(self.event_id),
            "request": self.request,
            "status": self.status.name,
            "data": self.data
        }


@dataclass
class DBRequest:
    event_id: uuid4
    parameter: str
    status: Status
    data: Optional[str] = None

    def __hash__(self) -> int:
        return hash(self.event_id)
