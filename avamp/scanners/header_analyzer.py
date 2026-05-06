class HeaderAnalyzer:
    async def scan(self, target: str) -> list[dict]:
        return [{"target": target, "type": "header_analysis", "evidence": "placeholder"}]
