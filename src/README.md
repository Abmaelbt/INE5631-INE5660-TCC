# AIOps Middleware

Este é o *middleware* proposto como prova de conceito para o TCC, responsável por interceptar dados de observabilidade e repassar para análises de modelos LLM.

## Como inicializar

1. Instale o [Poetry](https://python-poetry.org/docs/) caso não tenha (`sudo dnf install poetry` ou via `pipx`).
2. Acesse esta pasta.
3. Instale as dependências:
   ```bash
   poetry install
   ```
4. Crie seu ambiente de configuração copiando o `.env.example`:
   ```bash
   cp .env.example .env
   ```
5. Rode a aplicação FastAPI usando uvicorn:
   ```bash
   poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```
