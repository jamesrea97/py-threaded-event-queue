"""Module contains domain objects"""
from dataclasses import dataclass
from enum import Enum
from typing import Optional
from uuid import uuid4


class Status(Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    FINISHED = "FINISHED"


@dataclass
class DbResponse:
    id_: uuid4
    status: Status
    result: Optional[str]
    error: Optional[str]
    