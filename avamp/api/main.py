"""FastAPI entrypoint for AVAMP."""

from fastapi import FastAPI

app = FastAPI(title="AVAMP API", version="0.1.0")


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/scan")
async def trigger_scan() -> dict[str, str]:
    return {"message": "Scan request accepted (queue integration pending)."}


@app.post("/reports/hourly")
async def generate_hourly_report() -> dict[str, str]:
    return {"message": "Hourly report generation triggered (renderer pending)."}
