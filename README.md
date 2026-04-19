# Sistema de AIOps para Monitoramento e Análise de Causa Raiz de Incidentes em Servidores Cloud com LLMs

## Estrutura do Projeto

Este repositório está subdividido em duas partes principais:

- **`docs/latex/`**: Contém todo o projeto de texto da tese/monografia codificado em LaTeX. É aqui que você encontra os capítulos, referências, apêndices e configurações da ABNT. Para compilar o documento de forma limpa, acesse este diretório e utilize o `Makefile`.
  
- **`src/`**: Contém a prova de conceito (PoC) e a implementação prática do TCC. Aqui estarão armazenados os componentes da solução, como middlewares em Python, integração com ferramentas Open Source (Prometheus, LGTM) e chamadas às APIs de LLMs, bem como os arquivos de ambiente `.env`.

## Compilação do Documento LaTeX

```bash
cd docs/latex
make # Ou rode a rotina de build latexmk apropriada
```
