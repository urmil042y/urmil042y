"""Scheduling placeholders for recurring scan jobs."""

from dataclasses import dataclass


@dataclass
class ScheduleConfig:
    interval_minutes: int = 60
    prevent_overlap: bool = True


def describe_schedule(cfg: ScheduleConfig) -> str:
    overlap = "disabled" if cfg.prevent_overlap else "enabled"
    return f"Runs every {cfg.interval_minutes}m; overlapping scans {overlap}."
