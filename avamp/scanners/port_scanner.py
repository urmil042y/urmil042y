class PortScanner:
    async def scan(self, target: str) -> list[dict]:
        return [{"target": target, "type": "port_scan", "evidence": "placeholder"}]
