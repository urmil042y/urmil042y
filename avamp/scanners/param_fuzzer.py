class ParamFuzzer:
    async def scan(self, target: str) -> list[dict]:
        return [{"target": target, "type": "param_fuzz", "evidence": "placeholder"}]
