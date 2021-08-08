"""Module contains domain objects"""
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import uuid4


class Status(Enum):
    """Status of DBRequest"""
    TOO_BUSY = "TOO_BUSY"
    NOT_FOUND = "NOT_FOUND"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"


@dataclass
class DBRequest:
    """Represents request sent from DB."""
    event_id: uuid4
    parameter: str
    status: Status
    data: Optional[str] = None

    def __hash__(self) -> int:
        return hash(self.event_id)

    def to_json(self):
        return {
            "event_id": str(self.event_id),
            "parameter": self.parameter,
            "status": self.status.value,
            "data": self.data
        }


@dataclass
class DbResponse:
    """Represents request returned to Client."""
    event_id: uuid4
    db_request: DBRequest
    timestamp: datetime = datetime.now()

    def to_json(self):
        return {
            "datetime": str(self.timestamp),
            "event_id": str(self.event_id),
            "db_request": self.db_request.to_json()
        }
