"""Ethical API security testing tool for privacy-focused research."""

from __future__ import annotations

import asyncio
from pathlib import Path

import httpx

from avamp.research.api_client import ApiResearchClient
from avamp.research.logging_utils import configure_logger
from avamp.research.models import EndpointConfig, TestIdentity
from avamp.research.rate_limit_detector import RateLimitDetector
from avamp.research.reporting import build_markdown_report
from avamp.research.response_analyzer import ResponseAnalyzer


class ApiPrivacyResearchTool:
    def __init__(self, base_url: str, report_dir: str = "./reports"):
        self.logger = configure_logger()
        self.client = ApiResearchClient(
            base_url=base_url,
            user_agent="ApiPrivacyResearchTool/1.0 (+authorized-security-testing)",
        )
        self.response_analyzer = ResponseAnalyzer()
        self.rate_limit_detector = RateLimitDetector()
        self.report_dir = Path(report_dir)
        self.report_dir.mkdir(parents=True, exist_ok=True)

    async def run(
        self,
        target_name: str,
        endpoints: list[EndpointConfig],
        identities: list[TestIdentity],
    ) -> Path:
        self.logger.info(
            "starting_authorized_assessment",
            extra={"extra": {"target": target_name, "endpoint_count": len(endpoints)}},
        )

        async with httpx.AsyncClient() as http_client:
            outcomes = []
            for endpoint in endpoints:
                for identity in identities:
                    outcome = await self.client.probe_identity(
                        http_client,
                        endpoint,
                        identity,
                        payload_factory=lambda i: {"identifier": i.identifier},
                    )
                    outcomes.append(outcome)
                    self.logger.info(
                        "probe_completed",
                        extra={
                            "extra": {
                                "endpoint": endpoint.name,
                                "identity": identity.label,
                                "status": outcome.status_code,
                                "duration_ms": round(outcome.duration_ms, 2),
                            }
                        },
                    )

        findings = self.response_analyzer.analyze(outcomes)
        findings.extend(self.rate_limit_detector.evaluate(outcomes))
        report = build_markdown_report(target_name, outcomes, findings)

        report_path = self.report_dir / f"{target_name}_privacy_report.md"
        report_path.write_text(report)
        self.logger.info(
            "assessment_complete",
            extra={"extra": {"report_path": str(report_path), "findings": len(findings)}},
        )
        return report_path


def demo_run() -> None:
    """Demonstration run against authorized lab endpoints only."""

    tool = ApiPrivacyResearchTool(base_url="https://lab.example.local")
    endpoints = [
        EndpointConfig(name="password_recovery", path="/api/v1/auth/recover"),
        EndpointConfig(name="login", path="/api/v1/auth/login"),
    ]
    identities = [
        TestIdentity(label="known_test_account", identifier="researcher1@example.local", expected_exists=True),
        TestIdentity(label="unknown_control", identifier="no-user@example.local", expected_exists=False),
    ]
    asyncio.run(tool.run(target_name="lab_social_app", endpoints=endpoints, identities=identities))


if __name__ == "__main__":
    demo_run()
