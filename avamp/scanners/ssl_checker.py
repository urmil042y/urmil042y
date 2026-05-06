class SSLChecker:
    async def scan(self, target: str) -> list[dict]:
        return [{"target": target, "type": "ssl_check", "evidence": "placeholder"}]
