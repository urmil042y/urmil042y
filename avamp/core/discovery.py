"""Asset discovery and scope enforcement primitives."""

from dataclasses import dataclass
from ipaddress import ip_address, ip_network
from typing import Iterable


@dataclass(frozen=True)
class ScopePolicy:
    """Allowlist-based scope policy."""

    allowed_cidrs: tuple[str, ...]
    allowed_domains: tuple[str, ...]

    def is_ip_allowed(self, candidate: str) -> bool:
        ip = ip_address(candidate)
        return any(ip in ip_network(cidr) for cidr in self.allowed_cidrs)

    def is_domain_allowed(self, candidate: str) -> bool:
        return any(candidate == d or candidate.endswith(f".{d}") for d in self.allowed_domains)


def enforce_scope(targets: Iterable[str], policy: ScopePolicy) -> list[str]:
    """Return only authorized targets; raise when all are out of scope."""
    authorized: list[str] = []
    for target in targets:
        if target.replace(".", "").isdigit() and policy.is_ip_allowed(target):
            authorized.append(target)
        elif policy.is_domain_allowed(target):
            authorized.append(target)
    if not authorized:
        raise ValueError("No authorized targets in request.")
    return authorized
