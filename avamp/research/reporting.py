"""Reporting module for ethical API privacy research."""

from datetime import datetime, timezone

from avamp.research.models import Finding, RequestOutcome


def build_markdown_report(
    target_name: str,
    outcomes: list[RequestOutcome],
    findings: list[Finding],
) -> str:
    lines = [
        f"# API Privacy Research Report — {target_name}",
        "",
        f"Generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Scope & Safety Constraints",
        "- Executed only in authorized lab environment and/or against researcher-owned test accounts.",
        "- No authentication bypass, no data scraping, and no control-evasion logic was used.",
        "- Focus: OWASP-aligned defensive analysis of account enumeration exposure.",
        "",
        "## Observations",
    ]

    for finding in findings:
        lines.extend(
            [
                f"### {finding.category} ({finding.severity})",
                f"- Summary: {finding.summary}",
                f"- Evidence: `{finding.evidence}`",
                f"- Recommendation: {finding.recommendation}",
                "",
            ]
        )

    lines.extend(
        [
            "## Defensive Recommendations",
            "- Return generic error messages for all auth/recovery outcomes.",
            "- Keep status codes and response body schemas uniform.",
            "- Enforce consistent server-side timing envelopes.",
            "- Apply CAPTCHA and stronger checks under suspicious OTP/recovery activity.",
            "- Use layered throttling: IP, account, device fingerprint, and behavioral signals.",
            "- Monitor anomalies and alert on repeated enumeration-like patterns.",
            "",
            "## Raw Request Outcomes",
        ]
    )
    for outcome in outcomes:
        lines.append(
            f"- {outcome.endpoint_name}/{outcome.identity_label}: status={outcome.status_code}, "
            f"duration_ms={outcome.duration_ms:.1f}, classification={outcome.error_classification}, "
            f"attempt={outcome.attempt}"
        )

    return "\n".join(lines)
