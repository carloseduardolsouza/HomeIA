from typing import Any, Dict, List

from pydantic import BaseModel, Field


class IngestRequest(BaseModel):
    topic: str
    payload: Dict[str, Any]


class BatchIngestRequest(BaseModel):
    readings: List[IngestRequest] = Field(..., min_length=1, max_length=100)
