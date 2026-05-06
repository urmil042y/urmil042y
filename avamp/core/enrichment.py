"""CVE enrichment interfaces."""

from dataclasses import dataclass


@dataclass
class CveRecord:
    cve_id: str
    cvss_score: float | None
    summary: str


def map_finding_to_cve(technology: str, version: str) -> str:
    """Simple placeholder strategy for future matcher implementation."""
    return f"{technology}:{version}"
