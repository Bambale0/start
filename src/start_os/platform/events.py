from datetime import UTC, datetime
from typing import Any
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class DomainEvent(BaseModel):
    event_id: UUID = Field(default_factory=uuid4)
    event_type: str = Field(min_length=1)
    version: int = Field(default=1, ge=1)
    occurred_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    organization_id: UUID | None = None
    group_id: UUID | None = None

    aggregate_type: str = Field(min_length=1)
    aggregate_id: UUID

    actor_id: UUID | None = None
    request_id: str | None = None
    trace_id: str | None = None

    payload: dict[str, Any] = Field(default_factory=dict)
