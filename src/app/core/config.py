from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 8000
    
    # URLs Observability
    prometheus_url: str = "http://localhost:9090"
    loki_url: str = "http://localhost:3100"
    
    # LLM Settings
    ollama_url: str = "http://localhost:11434"
    gemini_api_key: str | None = None
    groq_api_key: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
