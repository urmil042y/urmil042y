"""Rate-limit and challenge trigger detection."""

from collections import Counter

from avamp.research.models import Finding, RequestOutcome


class RateLimitDetector:
    RATE_LIMIT_CODES = {429, 403}

    def evaluate(self, outcomes: list[RequestOutcome]) -> list[Finding]:
        findings: list[Finding] = []
        if not outcomes:
            return findings

        status_counts = Counter(o.status_code for o in outcomes)
        rate_hits = sum(status_counts.get(code, 0) for code in self.RATE_LIMIT_CODES)
        captcha_hits = sum(1 for o in outcomes if o.error_classification == "captcha")
        otp_changes = sum(1 for o in outcomes if o.error_classification == "otp")

        if rate_hits:
            findings.append(
                Finding(
                    category="rate_limiting",
                    severity="info",
                    summary="Protective rate limiting behavior observed.",
                    evidence={"rate_limit_responses": rate_hits, "status_distribution": dict(status_counts)},
                    recommendation="Ensure throttling thresholds are consistent across valid and invalid identities.",
                )
            )
        else:
            findings.append(
                Finding(
                    category="rate_limiting",
                    severity="medium",
                    summary="No explicit rate limiting responses detected.",
                    evidence={"status_distribution": dict(status_counts)},
                    recommendation="Add per-IP/per-account throttling and cooldowns for recovery/authentication endpoints.",
                )
            )

        if captcha_hits == 0:
            findings.append(
                Finding(
                    category="captcha",
                    severity="low",
                    summary="No CAPTCHA challenge indicators observed.",
                    evidence={"captcha_indicators": captcha_hits},
                    recommendation="Enforce adaptive CAPTCHA after suspicious OTP or recovery attempts.",
                )
            )
        if otp_changes:
            findings.append(
                Finding(
                    category="otp_flow",
                    severity="info",
                    summary="OTP workflow indicators were observed in responses.",
                    evidence={"otp_related_responses": otp_changes},
                    recommendation="Ensure OTP request responses are generic and do not disclose account existence.",
                )
            )
        return findings
