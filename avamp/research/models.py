"""Data models for ethical API privacy analysis research."""

from dataclasses import dataclass, field
from time import perf_counter
from typing import Any


@dataclass
class TestIdentity:
    """Represents a researcher-controlled test identity."""

    label: str
    identifier: str
    expected_exists: bool


@dataclass
class EndpointConfig:
    """Configuration for auth/recovery endpoint testing."""

    name: str
    path: str
    method: str = "POST"
    timeout_seconds: float = 20.0


@dataclass
class RequestOutcome:
    """Captured request/response data for differential analysis."""

    endpoint_name: str
    identity_label: str
    request_id: str
    status_code: int
    duration_ms: float
    body_excerpt: str
    headers: dict[str, str]
    attempt: int
    sent_at_monotonic: float = field(default_factory=perf_counter)
    error_classification: str = ""


@dataclass
class Finding:
    """Represents a possible enumeration/privacy signal."""

    category: str
    severity: str
    summary: str
    evidence: dict[str, Any]
    recommendation: str
