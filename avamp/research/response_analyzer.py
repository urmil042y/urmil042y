"""Response differential analysis for enumeration risk."""

from statistics import mean

from avamp.research.models import Finding, RequestOutcome


class ResponseAnalyzer:
    def __init__(self, timing_threshold_ms: float = 120.0):
        self.timing_threshold_ms = timing_threshold_ms

    def analyze(self, outcomes: list[RequestOutcome]) -> list[Finding]:
        findings: list[Finding] = []
        by_identity: dict[str, list[RequestOutcome]] = {}
        for outcome in outcomes:
            by_identity.setdefault(outcome.identity_label, []).append(outcome)

        if len(by_identity) < 2:
            return findings

        status_sets = {label: sorted({o.status_code for o in rows}) for label, rows in by_identity.items()}
        unique_sets = {tuple(v) for v in status_sets.values()}
        if len(unique_sets) > 1:
            findings.append(
                Finding(
                    category="status_code_diff",
                    severity="high",
                    summary="Different status code patterns detected between test identities.",
                    evidence={"status_by_identity": status_sets},
                    recommendation="Return a single generic status pattern for both existing and non-existing accounts.",
                )
            )

        body_markers = {
            label: sorted({o.error_classification for o in rows})
            for label, rows in by_identity.items()
        }
        if len({tuple(v) for v in body_markers.values()}) > 1:
            findings.append(
                Finding(
                    category="message_diff",
                    severity="high",
                    summary="Error message semantics differ across identities.",
                    evidence={"classifications": body_markers},
                    recommendation="Use generic error copy that does not reveal account existence or account state.",
                )
            )

        timing_profile = {label: mean(o.duration_ms for o in rows) for label, rows in by_identity.items()}
        if max(timing_profile.values()) - min(timing_profile.values()) > self.timing_threshold_ms:
            findings.append(
                Finding(
                    category="timing_side_channel",
                    severity="medium",
                    summary="Average response time differs beyond configured threshold.",
                    evidence={"avg_duration_ms": timing_profile, "threshold_ms": self.timing_threshold_ms},
                    recommendation="Normalize backend processing time and add jitter on server side to reduce timing oracles.",
                )
            )

        if not findings:
            findings.append(
                Finding(
                    category="uniformity",
                    severity="info",
                    summary="Responses appear largely uniform across provided test identities.",
                    evidence={"status_by_identity": status_sets, "avg_duration_ms": timing_profile},
                    recommendation="Continue regression testing to maintain anti-enumeration controls.",
                )
            )
        return findings
