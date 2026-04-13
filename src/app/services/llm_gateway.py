class LLMGateway:
    def __init__(self):
        pass

    async def analyze_incident(self, incident_context: dict, prompt_technique: str = "zero-shot") -> str:
        """
        Orquestra a chamada para o modelo (Ollama local ou Gemini/Groq via API).
        Recebe o contexto empacotado (alertas + métricas) e devolve a causa raiz proposta.
        """
        # Futura implementação de "Prompt Assembly"
        return f"Causa raiz sugerida (mock): Análise primária do alerta via {prompt_technique}."

llm_gateway = LLMGateway()
