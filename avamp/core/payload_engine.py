"""Payload library loading and request pacing utilities."""

from dataclasses import dataclass


@dataclass
class Payload:
    category: str
    value: str


def build_payload_record(payload: Payload, response_code: int, signal: str) -> dict[str, str | int]:
    return {
        "category": payload.category,
        "payload": payload.value,
        "response_code": response_code,
        "signal": signal,
    }
