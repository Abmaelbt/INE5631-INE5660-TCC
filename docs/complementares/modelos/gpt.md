# 1. Introdução

## 1.1 Contextualização

A computação em nuvem tornou-se um dos pilares da infraestrutura moderna de Tecnologia da Informação, oferecendo escalabilidade, elasticidade e flexibilidade para organizações de diferentes portes. Nesse contexto, ambientes de nuvem pública, como a Amazon Web Services (AWS), passaram a hospedar aplicações e serviços críticos para o negócio, cuja disponibilidade e desempenho impactam diretamente a experiência do usuário e os resultados da organização.

Paralelamente, a adoção de arquiteturas distribuídas, microsserviços e componentes desacoplados ampliou de forma significativa a complexidade operacional dos ambientes de produção. Uma única aplicação moderna pode envolver múltiplos serviços interdependentes, gerando um grande volume de métricas, registros de log e eventos de infraestrutura em curto intervalo de tempo. Diante desse cenário, equipes de operação, observabilidade e confiabilidade de software, especialmente aquelas atuando com práticas de DevOps e Site Reliability Engineering (SRE), enfrentam o desafio de monitorar, diagnosticar e responder a incidentes com agilidade e precisão.

O modelo tradicional de monitoramento, baseado principalmente em limiares estáticos e alertas reativos, mostra-se limitado para esse tipo de ambiente. Embora seja útil para indicar violações de parâmetros previamente definidos, esse modelo não é suficiente para interpretar o contexto do incidente, correlacionar sinais provenientes de diferentes fontes ou sugerir ações de mitigação. Como consequência, a atuação da equipe costuma ocorrer apenas após a degradação do serviço, o que eleva o Tempo Médio de Resolução (MTTR) e aumenta o impacto operacional.

Nesse contexto, o conceito de AIOps (Artificial Intelligence for IT Operations) surge como uma alternativa para apoiar a análise de grandes volumes de telemetria e reduzir a dependência de processos manuais. Em linhas gerais, AIOps busca aplicar técnicas de inteligência artificial, aprendizado de máquina e análise automatizada sobre dados de observabilidade, como métricas, logs e traces, com o objetivo de apoiar a detecção de anomalias, a correlação de eventos e a análise de causa raiz de incidentes.

Mais recentemente, os Modelos de Linguagem de Grande Escala (Large Language Models — LLMs) passaram a ser considerados como uma camada complementar relevante em cenários de AIOps. Esses modelos apresentam capacidade de interpretar linguagem natural, sintetizar informações e produzir explicações coerentes a partir de contexto estruturado ou semiestruturado. Quando integrados a pipelines de observabilidade, podem contribuir para a interpretação de alertas, a geração de hipóteses sobre a origem do problema e a sugestão de ações operacionais em linguagem acessível. Nesse sentido, técnicas de injeção de contexto, como Retrieval-Augmented Generation (RAG), Prompt Chaining e Few-Shot Prompting, ampliam a utilidade desses modelos ao fornecer informações relevantes para que as respostas sejam mais consistentes com a infraestrutura monitorada. Para viabilizar essa integração, este trabalho considera tanto a execução local de modelos quanto o consumo por APIs de inferência, de modo a comparar viabilidade, custo e desempenho.

## 1.2 Problema

Apesar da maturidade crescente das ferramentas de observabilidade open source, como Prometheus, Loki e Grafana, ainda existe uma lacuna entre a coleta de dados operacionais e a interpretação inteligente desses dados. Em geral, essas ferramentas são eficientes para centralizar métricas, armazenar registros e disponibilizar painéis de visualização, mas não realizam, de forma nativa, a inferência sobre a provável causa de um incidente nem recomendam ações corretivas de maneira automatizada.

Na prática, isso obriga as equipes de operação a conduzirem manualmente a análise de causa raiz, consultando diferentes painéis, filtros e consultas para reconstruir a sequência de eventos associados a uma falha. Esse processo é custoso, depende fortemente do conhecimento tácito da infraestrutura e tende a ser mais lento em cenários de alta pressão.

As soluções comerciais voltadas para AIOps e observabilidade inteligente oferecem recursos avançados de correlação e diagnóstico, mas normalmente apresentam barreiras relevantes de adoção, como custo de licenciamento, dependência de fornecedor e exigências específicas de integração. Além disso, parte dessas soluções exige o envio de dados operacionais para ambientes externos, o que pode ser um obstáculo em contextos com requisitos de segurança, conformidade ou restrições de privacidade.

No cenário open source, ainda são poucas as propostas que combinam, de forma integrada, um stack de observabilidade baseado em Prometheus, Loki e Grafana com LLMs aplicados à análise de causa raiz em linguagem natural. Também é limitada a disponibilidade de soluções que permitam diferentes formas de implantação do modelo, incluindo execução local ou consumo via API, sem comprometer a flexibilidade do ambiente. Essa lacuna define o problema de pesquisa que orienta o presente trabalho.

## 1.3 Objetivos

### 1.3.1 Objetivo Geral

Desenvolver e validar uma prova de conceito (PoC) de um sistema de AIOps que integre ferramentas de monitoramento open source a Modelos de Linguagem de Grande Escala (LLMs) para apoiar a análise de causa raiz (Root Cause Analysis — RCA) de alertas em servidores em nuvem, avaliando estratégias de implantação do modelo, incluindo execução local e consumo via APIs de inferência, com foco na viabilidade operacional e na qualidade dos diagnósticos gerados.

### 1.3.2 Objetivos Específicos

- Configurar uma pilha de monitoramento baseada em ferramentas open source em ambiente de nuvem, com foco na coleta de métricas de infraestrutura relevantes, como CPU, memória, disco e rede;

- Investigar técnicas de integração entre LLMs e dados de observabilidade, como Few-Shot Prompting, Prompt Chaining e Retrieval-Augmented Generation (RAG), avaliando sua adequação ao contexto de diagnóstico de incidentes;

- Desenvolver um middleware em Python capaz de interceptar alertas, consultar métricas e logs por meio de APIs e formatar o contexto de entrada para o LLM;

- Implementar a técnica de injeção de contexto selecionada na etapa de pesquisa, de modo a adaptar as respostas do modelo ao ambiente monitorado e reduzir respostas inconsistentes ou alucinações;

- Validar a prova de conceito por meio da simulação de incidentes controlados, avaliando utilidade, precisão e latência dos diagnósticos gerados pelo sistema.

## 1.4 Justificativa

A motivação para este trabalho pode ser compreendida em três dimensões complementares: prática, tecnológica e acadêmica.

Do ponto de vista prático, a proposta surge a partir de uma necessidade observada em um ambiente real de operação em nuvem, no qual a análise de incidentes ainda é realizada, em grande parte, de forma manual. Em cenários desse tipo, a equipe precisa reunir rapidamente informações dispersas em métricas, logs e alertas para entender a origem do problema, o que aumenta o tempo de resposta e eleva o esforço operacional. Uma solução de apoio à análise pode reduzir esse custo e tornar o processo de diagnóstico mais consistente.

Do ponto de vista tecnológico, os LLMs evoluíram significativamente nos últimos anos e passaram a ser utilizados em tarefas que exigem interpretação de texto, síntese de contexto e geração de explicações. Essa evolução tornou viável sua aplicação em problemas de observabilidade e AIOps, inclusive em abordagens que combinam dados estruturados de monitoramento com linguagem natural. Além disso, a possibilidade de uso tanto local quanto por API amplia a flexibilidade de implantação e permite comparar cenários com diferentes perfis de custo e desempenho.

Do ponto de vista acadêmico, o trabalho se justifica por investigar a aplicação de LLMs em um domínio ainda pouco consolidado na literatura de Sistemas de Informação, especialmente quando combinados com um stack de observabilidade open source e com foco em análise de causa raiz. A proposta contribui ao explorar uma arquitetura prática, flexível e aplicada, além de produzir uma análise comparativa entre diferentes estratégias de implantação do modelo.

## 1.5 Metodologia

A pesquisa possui natureza aplicada, pois busca desenvolver uma solução técnica para um problema operacional concreto. Quanto à abordagem, caracteriza-se como qualitativa e quantitativa: qualitativa na análise da utilidade dos diagnósticos produzidos e quantitativa na avaliação de métricas como tempo de resposta, taxa de acerto em cenários controlados e consistência das respostas geradas.

O método experimental será utilizado para desenvolvimento e validação da prova de conceito. O trabalho será conduzido nas seguintes etapas:

1. Revisão bibliográfica sobre AIOps, observabilidade, RCA, LLMs e técnicas de engenharia de prompt;
2. Definição da arquitetura da solução e dos componentes de monitoramento e integração;
3. Configuração do ambiente de monitoramento e da coleta de telemetria;
4. Desenvolvimento do middleware responsável por receber alertas e preparar o contexto para o LLM;
5. Integração do modelo de linguagem por execução local ou por API;
6. Simulação de incidentes e análise dos resultados obtidos.

## 1.6 Estrutura do Trabalho

O presente trabalho está organizado em capítulos. O Capítulo 1 apresenta a contextualização do problema, os objetivos, a justificativa e a metodologia adotada. O Capítulo 2 aborda a fundamentação teórica, incluindo conceitos de observabilidade, AIOps, LLMs e técnicas de injeção de contexto. O Capítulo 3 discute os trabalhos relacionados e posiciona a proposta em relação ao estado da arte. O Capítulo 4 descreve a arquitetura do protótipo proposto e as principais decisões de projeto. O Capítulo 5 detalha a implementação do middleware, a integração com o LLM e os componentes de observabilidade utilizados. O Capítulo 6 apresenta os cenários de validação e a análise dos resultados obtidos. Por fim, o Capítulo 7 retoma os objetivos do trabalho, discute as contribuições alcançadas, aponta limitações e indica possíveis trabalhos futuros.

## Referências deste capítulo

| Chave | Referência |
|---|---|
| [AWS, 2025] | Amazon Web Services. **What is AIOps?** Disponível em: https://aws.amazon.com/what-is/aiops/. Acesso em: 2025. |
| [IBM, 2025] | IBM. **What is AIOps?** Disponível em: https://www.ibm.com/think/topics/aiops. Acesso em: 2025. |
| [Gartner, 2025] | Gartner. **AIOps (Artificial Intelligence for IT Operations)**. Gartner Glossary. Disponível em: https://www.gartner.com/en/information-technology/glossary/aiops-artificial-intelligence-operations. Acesso em: 2025. |
| [Moura, 2024] | MOURA, Alysson Cristiano Estevam de. **Detecção e Interpretação de Anomalias em Logs de Sistemas de TI por meio de Inteligência Artificial**. Dissertação (Mestrado Profissional em Computação Aplicada) — Universidade de Brasília, Brasília, 2024. |
| [survey_llm_aiops, 2024] | A Survey of AIOps in the Era of Large Language Models. ACM Computing Surveys, 2024. DOI: 10.1145/3746635. |

