# 1. Introdução

## 1.1 Contextualização

A computação em nuvem consolidou-se como a espinha dorsal da infraestrutura de Tecnologia da Informação moderna, oferecendo escalabilidade, elasticidade e flexibilidade para organizações de todos os portes [AWS, 2025]. Nesse cenário, ambientes de nuvem pública, como a Amazon Web Services (AWS), tornaram-se plataformas essenciais para a hospedagem de serviços e aplicações críticas de negócio, cuja disponibilidade e desempenho impactam diretamente a experiência do usuário e os resultados financeiros das organizações.

Em paralelo, a crescente adoção de arquiteturas de microsserviços e infraestruturas distribuídas amplificou significativamente a complexidade operacional desses ambientes. Uma única aplicação moderna pode ser composta por dezenas de serviços interdependentes, gerando milhares de métricas por minuto e gigabytes de registros de log diariamente. Diante desse volume, as equipes de operações de TI — em especial as equipes de *Site Reliability Engineering* (SRE) e DevOps — enfrentam o desafio crescente de monitorar, diagnosticar e resolver incidentes em tempo hábil [IBM, 2025].

O modelo tradicional de monitoramento, baseado na definição de limiares estáticos para disparo de alertas — como notificar quando o consumo de CPU excede 90% — demonstra-se insuficiente para garantir a alta disponibilidade exigida pelos serviços atuais. Esse modelo reativo implica que a atuação técnica ocorre apenas após a manifestação do problema ou a degradação do serviço, elevando o Tempo Médio de Resolução (MTTR) e aumentando o risco de impacto ao usuário final.

Nesse contexto, o conceito de *AIOps* (Artificial Intelligence for IT Operations), definido pelo Gartner como a aplicação de técnicas de inteligência artificial e aprendizado de máquina às operações de TI, emerge como resposta ao problema da sobrecarga de dados operacionais [Gartner, 2025]. A incorporação de técnicas de aprendizado de máquina e análise estatística aos dados de telemetria — métricas, *logs* e rastros (*traces*) — permite não apenas identificar o estado atual da infraestrutura, mas correlacionar eventos e orientar diagnósticos de forma automatizada.

Recentemente, o avanço dos Modelos de Linguagem de Grande Escala (do inglês *Large Language Models* — LLMs), como a família Llama, Mistral e Qwen, abriu novas perspectivas para a área de AIOps. Esses modelos demonstraram capacidade significativa de raciocínio lógico sobre dados não estruturados, como registros de *log*, e podem ser utilizados para interpretar eventos detectados e sugerir causas prováveis de falhas em linguagem natural [Moura, 2024]. Combinados com técnicas de injeção de contexto, como a Geração com Recuperação Aumentada (do inglês *Retrieval-Augmented Generation* — RAG) e encadeamento de *prompts* (*Prompt Chaining*), esses modelos apresentam potencial para automatizar e enriquecer o processo de Análise de Causa Raiz (do inglês *Root Cause Analysis* — RCA) de incidentes em infraestruturas de nuvem. Para viabilizar essa integração, diferentes estratégias de implantação são exploradas neste trabalho, incluindo a execução local de modelos quantizados e o consumo de modelos por meio de APIs de inferência, permitindo avaliar o equilíbrio entre custo, privacidade e desempenho em cada abordagem.

---

## 1.2 Problema

A despeito dos avanços em ferramentas de observabilidade *open source*, como Prometheus, Loki e Grafana — que compõem o *stack* conhecido como LGTM (*Loki, Grafana, Tempo, Mimir*) —, essas soluções são eficientes na coleta e visualização de dados, mas não na sua interpretação. O Prometheus, por exemplo, é capaz de registrar que o consumo de CPU de uma instância atingiu 95%, mas não oferece mecanismos nativos para inferir a causa desse comportamento, correlacioná-lo com eventos em outros serviços ou sugerir ações de remediação.

Esse vácuo entre coleta de dados e diagnóstico inteligente força as equipes de operações a realizarem a análise de causa raiz de forma predominantemente manual, consultando individualmente painéis de métricas, *logs* e rastros para construir uma narrativa do incidente. Esse processo é lento, dependente de conhecimento especializado da infraestrutura e altamente suscetível a erros em cenários de alta pressão.

As soluções comerciais de AIOps que se propõem a resolver esse problema — como Datadog AI Ops, Dynatrace Davis e AWS DevOps Guru — apresentam dois obstáculos relevantes para adoção em ambientes corporativos de médio porte: o custo elevado de licenciamento e a dependência de fornecedor (*vendor lock-in*). Além disso, essas plataformas exigem o envio de dados operacionais para infraestruturas externas, o que pode representar impedimentos de conformidade e segurança da informação para diversas organizações.

No âmbito das soluções *open source*, embora existam iniciativas como o Keep (keephq), voltadas à correlação de alertas, ainda não há uma solução consolidada que integre modelos de linguagem de grande escala ao *stack* LGTM para diagnóstico automatizado de causa raiz em linguagem natural, com arquitetura flexível que suporte tanto execução local quanto consumo via APIs de inferência de baixo custo. Essa lacuna define o problema de pesquisa que norteia o presente trabalho.

---

## 1.3 Objetivos

### 1.3.1 Objetivo Geral

Desenvolver e validar uma prova de conceito (PoC) de um sistema de AIOps que integre ferramentas de monitoramento *open source* (Prometheus e LGTM) a Modelos de Linguagem de Grande Escala (LLMs) para automatizar e enriquecer a Análise de Causa Raiz (RCA) de alertas em servidores *cloud*, avaliando estratégias de implantação do modelo — incluindo execução local via Ollama e consumo por APIs de inferência — com foco na viabilidade operacional e na qualidade dos diagnósticos gerados.

### 1.3.2 Objetivos Específicos

- Configurar a pilha de monitoramento baseada em ferramentas *open source* (Prometheus e LGTM) em ambiente de servidores *cloud* (AWS), coletando as quatro métricas douradas de infraestrutura: CPU, memória, disco e rede;

- Investigar e comparar técnicas de integração entre LLMs e dados de observabilidade, tais como *Few-Shot Prompting*, *Prompt Chaining* e Geração com Recuperação Aumentada (RAG), avaliando o desempenho de diferentes modelos *open source* em tarefas de diagnóstico de incidentes;

- Desenvolver um *middleware* (script de automação em Python) capaz de interceptar alertas do Alertmanager, extrair métricas de contexto via API do Prometheus e Loki, e formatar as requisições para o LLM;

- Implementar a técnica de injeção de contexto selecionada na etapa de pesquisa no *middleware*, adaptando as respostas do modelo à infraestrutura local e validando a mitigação de alucinações;

- Validar a prova de conceito por meio da simulação de incidentes controlados (como esgotamento de memória e picos de CPU), avaliando a utilidade, precisão e latência dos diagnósticos gerados pelo sistema.

---

## 1.4 Justificativa

A motivação para o desenvolvimento deste trabalho assenta-se em três dimensões complementares: prática, tecnológica e acadêmica.

Do ponto de vista **prático**, o trabalho nasce de uma necessidade operacional identificada no ambiente profissional do autor, que atua com infraestrutura em nuvem AWS monitorada pelo *stack* Prometheus e LGTM. O processo de diagnóstico de incidentes nesse ambiente é predominantemente manual, demandando tempo e conhecimento especializado que nem sempre estão disponíveis no momento do incidente. Essa realidade é compartilhada por grande parte das equipes de engenharia de infraestrutura de médio porte no Brasil, que não dispõem de orçamento para soluções comerciais de AIOps.

Do ponto de vista **tecnológico**, os LLMs *open source* atingiram, entre 2023 e 2025, um nível de capacidade que os torna viáveis para tarefas especializadas mesmo em hardware de consumidor, graças a técnicas de quantização como QLoRA e GGUF. Modelos como Llama 3, Mistral e Qwen demonstraram desempenho competitivo em tarefas de raciocínio lógico e análise de dados não estruturados [survey_llm_aiops, 2024], e podem ser consumidos tanto localmente quanto por meio de APIs de inferência de baixo custo — como Groq e Gemini — abrindo uma janela de oportunidade para sua aplicação em contextos de AIOps com diferentes perfis de hardware e orçamento.

Do ponto de vista **acadêmico**, a revisão da literatura brasileira não identificou trabalhos no âmbito de Sistemas de Informação que combinem RAG ou técnicas equivalentes de injeção de contexto com dados de observabilidade do *stack* Prometheus e LGTM para diagnóstico de causa raiz com LLMs, em arquitetura flexível que suporte múltiplas estratégias de implantação. Essa lacuna, somada à contribuição metodológica de comparar execução local e consumo via API, representa a principal contribuição do presente trabalho.

---

## 1.5 Metodologia

A pesquisa classifica-se como **aplicada** quanto à sua natureza, pois objetiva o desenvolvimento de uma solução técnica para um problema operacional concreto. Quanto à abordagem, é **quantitativa e qualitativa**: quantitativa na avaliação de métricas objetivas dos diagnósticos gerados (precisão, latência e taxa de alucinações), e qualitativa na análise da utilidade e relevância das causas raiz identificadas pelo sistema.

O método experimental será utilizado para o desenvolvimento e validação da Prova de Conceito (PoC). O trabalho é estruturado nas seguintes etapas:

1. **Revisão Bibliográfica:** Levantamento do estado da arte sobre AIOps, RCA, LLMs *open source*, técnicas de engenharia de *prompt* (RAG, *Few-Shot Prompting*, *Prompt Chaining*) e monitoramento de infraestrutura em nuvem;

2. **Configuração do Ambiente:** Preparação da infraestrutura na AWS (instâncias EC2) e instalação das ferramentas de coleta de telemetria (Prometheus, Alertmanager, Loki, Grafana e *exporters*);

3. **Desenvolvimento do Middleware:** Implementação do script Python de integração entre o Alertmanager e o LLM, incluindo a camada de extração de contexto via APIs do Prometheus e Loki;

4. **Implementação e Refinamento:** Aplicação da técnica de injeção de contexto selecionada, refinamento dos *prompts* e testes funcionais com múltiplas estratégias de implantação do LLM (execução local via Ollama e consumo via APIs de inferência como Groq e Gemini);

5. **Validação e Análise:** Simulação controlada de incidentes, coleta dos diagnósticos gerados pelo sistema e avaliação comparativa dos resultados em relação a critérios predefinidos de qualidade e desempenho.

---

## 1.6 Estrutura do Trabalho

O presente trabalho está organizado em sete capítulos. O Capítulo 1 apresenta a contextualização do problema, os objetivos, a justificativa e a metodologia adotada. O Capítulo 2 desenvolve a fundamentação teórica, abordando os conceitos de observabilidade, AIOps, Modelos de Linguagem de Grande Escala e as técnicas de engenharia de *prompt* investigadas. O Capítulo 3 discute os trabalhos relacionados, posicionando a proposta deste trabalho em relação ao estado da arte. O Capítulo 4 descreve a arquitetura do protótipo proposto e as decisões de projeto. O Capítulo 5 detalha o processo de implementação do *middleware*, da camada de injeção de contexto e da integração com o LLM, incluindo as estratégias de implantação avaliadas. O Capítulo 6 apresenta os cenários de validação, os resultados obtidos e a análise comparativa. Por fim, o Capítulo 7 retoma os objetivos do trabalho, discute as contribuições alcançadas, as limitações identificadas e propõe direções para trabalhos futuros.

---

## Referências deste capítulo

| Chave | Referência |
|---|---|
| [AWS, 2025] | Amazon Web Services. **What is AIOps?** Disponível em: https://aws.amazon.com/what-is/aiops/. Acesso em: 2025. |
| [IBM, 2025] | IBM. **What is AIOps?** Disponível em: https://www.ibm.com/think/topics/aiops. Acesso em: 2025. |
| [Gartner, 2025] | Gartner. **AIOps (Artificial Intelligence for IT Operations)**. Gartner Glossary. Disponível em: https://www.gartner.com/en/information-technology/glossary/aiops-artificial-intelligence-operations. Acesso em: 2025. |
| [Moura, 2024] | MOURA, Alysson Cristiano Estevam de. **Detecção e Interpretação de Anomalias em Logs de Sistemas de TI por meio de Inteligência Artificial**. Dissertação (Mestrado Profissional em Computação Aplicada) — Universidade de Brasília, Brasília, 2024. |
| [survey_llm_aiops, 2024] | A Survey of AIOps in the Era of Large Language Models. ACM Computing Surveys, 2024. DOI: 10.1145/3746635. *(completar com autores após acesso ao artigo)* |