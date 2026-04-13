import httpx
from app.core.config import settings

class PrometheusClient:
    def __init__(self):
        self.base_url = settings.prometheus_url

    async def query(self, promql_query: str):
        """Busca dados no Prometheus via HTTP"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/api/v1/query",
                    params={"query": promql_query}
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"Erro ao acessar Prometheus: {e}")
                return None
