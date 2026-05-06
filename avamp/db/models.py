"""Persistence model stubs for AVAMP."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Asset:
    id: int
    target: str
    target_type: str
    in_scope: bool


@dataclass
class Finding:
    id: int
    asset_id: int
    severity: str
    title: str
    details: str
    discovered_at: datetime
