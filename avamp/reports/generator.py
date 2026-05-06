"""Report model and delta calculation helpers."""

from collections.abc import Iterable


def finding_key(finding: dict) -> tuple:
    return finding.get("target"), finding.get("type"), finding.get("evidence")


def calculate_delta(previous: Iterable[dict], current: Iterable[dict]) -> dict[str, list[dict]]:
    prev_map = {finding_key(f): f for f in previous}
    curr_map = {finding_key(f): f for f in current}

    new_keys = curr_map.keys() - prev_map.keys()
    resolved_keys = prev_map.keys() - curr_map.keys()

    return {
        "new": [curr_map[k] for k in new_keys],
        "resolved": [prev_map[k] for k in resolved_keys],
    }
