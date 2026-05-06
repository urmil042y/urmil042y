"""Central scanner orchestration."""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass
class ScanResult:
    target: str
    scanner: str
    findings: list[dict[str, Any]]
    scanned_at: datetime


class ScanOrchestrator:
    """Dispatches scanner modules and aggregates results."""

    def __init__(self, scanners: dict[str, Any]):
        self.scanners = scanners

    async def run_cycle(self, targets: list[str]) -> list[ScanResult]:
        results: list[ScanResult] = []
        for target in targets:
            for name, scanner in self.scanners.items():
                findings = await scanner.scan(target)
                results.append(
                    ScanResult(
                        target=target,
                        scanner=name,
                        findings=findings,
                        scanned_at=datetime.now(timezone.utc),
                    )
                )
        return results
