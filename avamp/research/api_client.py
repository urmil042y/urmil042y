"""Async API client for authorized security research probes."""

from __future__ import annotations

import asyncio
import random
import uuid
from typing import Any

import httpx

from avamp.research.models import EndpointConfig, RequestOutcome, TestIdentity


class ApiResearchClient:
    def __init__(
        self,
        base_url: str,
        user_agent: str,
        min_delay_seconds: float = 0.3,
        max_delay_seconds: float = 1.2,
        retries: int = 2,
    ):
        self.base_url = base_url.rstrip("/")
        self.user_agent = user_agent
        self.min_delay_seconds = min_delay_seconds
        self.max_delay_seconds = max_delay_seconds
        self.retries = retries

    async def probe_identity(
        self,
        client: httpx.AsyncClient,
        endpoint: EndpointConfig,
        identity: TestIdentity,
        payload_factory: Any,
    ) -> RequestOutcome:
        attempt = 0
        last_exc: Exception | None = None
        while attempt <= self.retries:
            attempt += 1
            request_id = str(uuid.uuid4())
            delay = random.uniform(self.min_delay_seconds, self.max_delay_seconds)
            await asyncio.sleep(delay)

            try:
                response = await client.request(
                    endpoint.method,
                    f"{self.base_url}{endpoint.path}",
                    json=payload_factory(identity),
                    headers={"User-Agent": self.user_agent, "X-Research-Request-ID": request_id},
                    timeout=endpoint.timeout_seconds,
                )
                body_excerpt = response.text[:300].replace("\n", " ")
                return RequestOutcome(
                    endpoint_name=endpoint.name,
                    identity_label=identity.label,
                    request_id=request_id,
                    status_code=response.status_code,
                    duration_ms=response.elapsed.total_seconds() * 1000,
                    body_excerpt=body_excerpt,
                    headers={k.lower(): v for k, v in response.headers.items()},
                    attempt=attempt,
                    error_classification=_classify_error(body_excerpt),
                )
            except (httpx.TimeoutException, httpx.TransportError) as exc:
                last_exc = exc
                if attempt > self.retries:
                    raise
        raise RuntimeError(f"Probe failed: {last_exc}")


def _classify_error(body_text: str) -> str:
    text = body_text.lower()
    if "captcha" in text:
        return "captcha"
    if "otp" in text or "one-time" in text:
        return "otp"
    if "rate limit" in text or "too many" in text:
        return "rate_limit"
    if "invalid" in text or "not found" in text:
        return "credential_or_identity"
    return "generic"
