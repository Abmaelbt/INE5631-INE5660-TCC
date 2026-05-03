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



# 2. Fundamentação Teórica

## 2.1 Observabilidade

A crescente complexidade dos sistemas de software modernos, especialmente aqueles baseados em arquiteturas de microsserviços e infraestruturas em nuvem, impôs novos desafios à engenharia de operações de TI. Nesse contexto, o conceito de observabilidade emergiu como um pilar fundamental para a compreensão do comportamento interno de sistemas a partir de seus dados externos [Wang et al., 2025]. Diferentemente do monitoramento tradicional — que verifica se um sistema está funcionando — a observabilidade busca responder *por que* ele se comporta de determinada maneira, permitindo diagnósticos mais precisos e ações mais eficazes diante de falhas [Zhang et al., 2025].

A literatura consolidada na área estrutura a observabilidade em torno de três tipos fundamentais de dados de telemetria, coletivamente conhecidos como os três pilares da observabilidade: métricas, logs e rastros (*traces*) [Zhang et al., 2025; Wang et al., 2025]. Cada pilar captura uma dimensão distinta do comportamento do sistema e, quando correlacionados, fornecem uma visão abrangente e contextualizada do estado da infraestrutura.

---

### 2.1.1 Métricas

As métricas são medições quantitativas coletadas continuamente de componentes da infraestrutura de TI, como uso de CPU, utilização de memória, I/O de disco, latência de rede e throughput [Zhang et al., 2025]. Por sua natureza numérica e temporal, constituem séries temporais que permitem a identificação de tendências, padrões sazonais e desvios em relação ao comportamento esperado do sistema.

No contexto do presente trabalho, as métricas representam a principal fonte de dados para o disparo de alertas. O Prometheus — ferramenta *open source* amplamente adotada em ambientes *cloud* e considerada padrão de facto para coleta de métricas em infraestruturas baseadas em Kubernetes e AWS [Wang et al., 2025] — é responsável pela raspagem periódica de dados expostos por *exporters* instalados nas instâncias EC2. As métricas coletadas abrangem as quatro métricas douradas de infraestrutura: latência, tráfego, erros e saturação [Wang et al., 2025], mapeadas operacionalmente para CPU, memória, disco e rede.

O modelo de alerta adotado, baseado em limiares estáticos (*threshold-based alerting*), é reconhecido na literatura como insuficiente para ambientes dinâmicos e distribuídos [Wang et al., 2025; Zhang et al., 2025]. É justamente essa limitação que motiva a integração com modelos de linguagem: ao receber um alerta do Alertmanager — componente responsável pelo roteamento e notificação de alertas do Prometheus —, o sistema proposto não apenas registra a ocorrência, mas busca contextualizar a métrica anômala com outros dados de telemetria para gerar um diagnóstico de causa raiz.

---

### 2.1.2 Logs

Os logs são registros detalhados e sequenciais de eventos que ocorrem dentro do sistema, abrangendo mensagens de erro, registros de transações, atividades de componentes e operações de infraestrutura [Zhang et al., 2025]. Sua natureza predominantemente não estruturada — composta por texto livre gerado por aplicações, sistemas operacionais e serviços — os torna ao mesmo tempo ricos em informação contextual e desafiadores para análise automatizada.

Wang et al. (2025) descrevem os logs como eventos estruturados e semiestruturados emitidos por código de aplicação e componentes de infraestrutura, destacando a importância da correlação entre logs e rastros de requisição para vincular entradas individuais a execuções específicas. Essa correlação é especialmente relevante em ambientes de microsserviços, onde uma única falha pode propagar mensagens de erro em múltiplos serviços simultaneamente.

No presente trabalho, o Loki — componente do *stack* LGTM responsável pelo armazenamento e indexação de logs — é utilizado como fonte secundária de contexto para o sistema de RCA. Quando um alerta é disparado pelo Prometheus, o *middleware* desenvolvido consulta a API do Loki para recuperar os registros de log dos serviços afetados no intervalo de tempo correspondente ao incidente. Essa janela temporal de coleta — tipicamente ±15 minutos ao redor do evento detectado, conforme proposto por Wang et al. (2025) — reduz significativamente o volume de dados sem comprometer a completude do contexto diagnóstico.

A capacidade dos LLMs de processar dados não estruturados como logs sem extração prévia de *features* é destacada por Zhang et al. (2025) como uma das vantagens centrais dessa abordagem em relação aos métodos tradicionais de AIOps, que exigem extenso pré-processamento e são pouco generalizáveis a diferentes formatos de log.

---

### 2.1.3 Rastros (*Traces*)

Os rastros capturam a sequência completa de operações ou transações que uma requisição percorre em um sistema distribuído [Zhang et al., 2025]. Em arquiteturas de microsserviços, uma única requisição do usuário pode atravessar dezenas de serviços antes de ser respondida. Os rastros — compostos por *spans* que representam operações individuais, anotados com informações de tempo, metadados e relações causais — oferecem visibilidade sobre as interações entre serviços, auxiliando na identificação de gargalos de desempenho, dependências e causas raiz de falhas em componentes específicos [Wang et al., 2025].

Wang et al. (2025) descrevem a construção de grafos dinâmicos de dependência de serviços a partir de rastros distribuídos, nos quais nós representam instâncias de microsserviços e arestas codificam relações de chamada ponderadas por frequência e latência. Redes neurais de grafos analisam essas estruturas para identificar padrões anômalos nas interações entre serviços.

No contexto deste trabalho, os rastros representam um dado de telemetria complementar, disponível por meio do componente Tempo do *stack* LGTM. Entretanto, sua integração com LLMs permanece como uma das fronteiras abertas da área — Zhang et al. (2025) identificam a ausência de trabalhos que utilizem dados de rastros de forma eficaz em abordagens baseadas em LLMs como uma das principais lacunas da literatura atual. Dessa forma, o presente trabalho delimita seu escopo ao uso de métricas e logs como fontes primárias de contexto para o sistema de RCA, apontando a integração com rastros como direção para trabalhos futuros.

---

### 2.1.4 O *stack* LGTM e o padrão OpenTelemetry

A correlação eficaz dos três pilares de observabilidade exige uma infraestrutura de coleta, armazenamento e consulta integrada. O OpenTelemetry emergiu como o padrão de facto para observabilidade em ambientes *cloud-native*, fornecendo instrumentação independente de fornecedor para coleta unificada de métricas, logs e rastros [Wang et al., 2025]. O projeto é mantido pela Cloud Native Computing Foundation (CNCF) e adotado amplamente pela indústria como base para pipelines de telemetria interoperáveis.

No presente trabalho, o *stack* LGTM — acrônimo para Loki, Grafana, Tempo e Mimir — é utilizado como plataforma de observabilidade *open source*, complementado pelo Prometheus para coleta de métricas e pelo Alertmanager para roteamento de alertas. Essa combinação de ferramentas constitui uma alternativa consolidada e sem custo de licenciamento às plataformas comerciais de observabilidade, viabilizando a proposta deste trabalho em ambientes corporativos com restrições orçamentárias.

O Grafana, componente de visualização do *stack*, serve como interface de acompanhamento do sistema de monitoramento e ponto de integração para notificações, enquanto o Alertmanager é configurado como *webhook* de entrada para o *middleware* Python desenvolvido neste trabalho — recebendo alertas estruturados e iniciando o pipeline de coleta de contexto e geração de diagnóstico pelo LLM.

A Figura 2.1 ilustra a relação entre os componentes do *stack* de observabilidade e o sistema proposto neste trabalho.

```
┌─────────────────────────────────────────────────────────┐
│                  Stack de Observabilidade               │
│                                                         │
│   Instâncias EC2                                        │
│   ┌──────────┐    métricas    ┌───────────┐            │
│   │ Exporters│ ─────────────► │ Prometheus│            │
│   └──────────┘                └─────┬─────┘            │
│                                     │ alerta            │
│   ┌──────────┐     logs       ┌─────▼──────────┐       │
│   │  Serviços│ ─────────────► │  Alertmanager  │       │
│   └──────────┘                └────────┬───────┘       │
│                                        │ webhook        │
│   ┌──────────┐     traces     ┌────────▼───────┐       │
│   │  Loki    │◄───────────────│   Middleware   │       │
│   │  Tempo   │  contexto      │    (Python)    │       │
│   └──────────┘ ◄──────────────└────────┬───────┘       │
│                                        │ prompt         │
│                               ┌────────▼───────┐       │
│                               │   LLM (local   │       │
│                               │   ou via API)  │       │
│                               └────────┬───────┘       │
│                               diagnóstico em            │
│                               linguagem natural         │
└─────────────────────────────────────────────────────────┘
```

*Figura 2.1: Relação entre o stack de observabilidade e o sistema proposto.*

---

### 2.1.5 Limitações do monitoramento baseado em limiares

O modelo tradicional de monitoramento, baseado em limiares estáticos para disparo de alertas, apresenta limitações estruturais que motivam diretamente a proposta deste trabalho. Wang et al. (2025) destacam que abordagens baseadas em regras predefinidas e alertas por limiar têm dificuldades em lidar com a natureza dinâmica e complexa dos sistemas *cloud-native*. O volume massivo de dados de telemetria — métricas, logs e rastros distribuídos — gerado por arquiteturas de microsserviços representa uma carga cognitiva substancial para operadores humanos.

Zhang et al. (2025) complementam essa análise ao identificar cinco limitações centrais das abordagens tradicionais de AIOps: a necessidade de engenharia de *features* complexa, a falta de generalidade entre plataformas, a ausência de flexibilidade entre tarefas, a adaptabilidade limitada diante de mudanças no sistema e os níveis restritos de automação. Essas limitações são especialmente críticas em contextos onde a resposta a incidentes deve ocorrer em segundos e o conhecimento sobre a infraestrutura específica nem sempre está disponível no momento da falha.

É nesse espaço — entre a riqueza de dados disponíveis nas ferramentas de observabilidade e a capacidade humana de interpretá-los sob pressão — que o presente trabalho propõe a aplicação de Modelos de Linguagem de Grande Escala para automação e enriquecimento da Análise de Causa Raiz.

---

## Referências desta seção

| Chave | Referência |
|---|---|
| [Zhang et al., 2025] | ZHANG, Lingzhe et al. **A Survey of AIOps in the Era of Large Language Models**. Journal of the ACM, v. 37, n. 4, art. 111, ago. 2025. arXiv:2507.12472v1. |
| [Wang et al., 2025] | WANG, Chen et al. **Integrating Large Language Models with Cloud-Native Observability for Automated Root Cause Analysis and Remediation**. In: AISNS 2025 — 3rd International Conference on Artificial Intelligence, Systems and Network Security, Xiangtan, China. ACM, 2025. DOI: 10.1145/3797161.3797213. |