from fastapi import APIRouter, HTTPException
from app.models.alert import AlertmanagerPayload
from app.services.prometheus_client import PrometheusClient
from app.services.llm_gateway import llm_gateway

router = APIRouter()
prom_client = PrometheusClient()

@router.post("/alert")
async def alertmanager_webhook(payload: AlertmanagerPayload):
    """
    Rota Webhook para receber chamadas do Alertmanager.
    """
    print(f"Recebido payload com status: {payload.status} e {len(payload.alerts)} alertas.")
    
    # Exemplo: prom_data = await prom_client.query("sum(rate(node_cpu_seconds_total[5m]))")
    
    # Orquestrar com o LLM (Mock inicial)
    analysis = await llm_gateway.analyze_incident(
        incident_context={"status": payload.status, "alerts": payload.alerts}
    )
    
    return {"status": "success", "ai_analysis": analysis}
