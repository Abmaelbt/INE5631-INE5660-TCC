from fastapi import FastAPI
from app.api.webhooks import router as webhooks_router

app = FastAPI(
    title="AIOps Middleware",
    description="RCA Middleware integrating Alertmanager, Prometheus/Loki and LLMs",
    version="1.0.0"
)

# Registra a rota do Webhook
app.include_router(webhooks_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "online"}
