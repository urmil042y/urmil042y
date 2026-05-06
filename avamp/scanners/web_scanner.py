class WebScanner:
    async def scan(self, target: str) -> list[dict]:
        return [{"target": target, "type": "web_scan", "evidence": "placeholder"}]
