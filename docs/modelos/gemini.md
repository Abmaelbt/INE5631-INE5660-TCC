1. INTRODUÇÃO

A crescente adoção de arquiteturas baseadas em computação em nuvem e microsserviços trouxe escalabilidade e resiliência sem precedentes para os sistemas de tecnologia da informação. No entanto, essa evolução arquitetural resultou em um aumento exponencial na complexidade do monitoramento e na volumetria de dados de telemetria gerados diariamente. Ferramentas de observabilidade modernas, como o ecossistema Prometheus e a pilha LGTM (Loki, Grafana, Tempo, Mimir), tornaram-se indispensáveis para coletar métricas, logs e traces. Apesar de eficientes na detecção de anomalias, essas ferramentas tradicionais operam em um modelo essencialmente reativo, baseado na violação de limiares estáticos (thresholds).

Nesse cenário, as equipes de operações e Engenharia de Confiabilidade de Sites (SRE) frequentemente se deparam com o fenômeno conhecido como "fadiga de alertas" (alert fatigue). Quando um incidente ocorre em ambientes distribuídos de larga escala, a alta densidade de notificações geradas em cascata carece de contexto unificado, exigindo que os engenheiros realizem a correlação manual de logs e métricas espalhados por diversos painéis. Esse processo investigativo manual eleva drasticamente o Tempo Médio de Reparação (MTTR), resultando em maiores períodos de indisponibilidade e degradação de serviços críticos. A Análise de Causa Raiz (RCA) torna-se, portanto, o principal gargalo na resolução de incidentes.

Para mitigar esse problema, o campo de AIOps (Artificial Intelligence for IT Operations) tem evoluído do uso de técnicas clássicas de aprendizado de máquina (Machine Learning) para a adoção de Modelos de Linguagem de Grande Escala (LLMs). A capacidade da Inteligência Artificial Generativa de interpretar linguagem natural e correlacionar vastas quantidades de texto permite que os LLMs atuem como assistentes operacionais investigativos, consumindo dados de telemetria brutos e gerando diagnósticos legíveis e contextualizados no exato momento em que um alerta é disparado.

Apesar do potencial demonstrado pelos LLMs na resolução de incidentes, a adoção corporativa exige arquiteturas flexíveis. Soluções rigidamente acopladas a provedores comerciais específicos podem gerar dependência tecnológica (vendor lock-in) e custos imprevisíveis em cenários de alta volumetria de alertas. Torna-se imperativa a investigação de arquiteturas desacopladas, que utilizem técnicas robustas de injeção de contexto — como Few-Shot Prompting ou Retrieval-Augmented Generation (RAG). Essa abordagem permite construir um middleware agnóstico, viabilizando o enriquecimento automatizado de alertas tanto através de modelos de código aberto executados localmente (garantindo privacidade de dados sensíveis) quanto por meio de APIs de nuvem de alta performance (para diagnósticos complexos), garantindo a viabilidade de execução em diferentes cenários operacionais.

1.1. Objetivos

1.1.1. Objetivo Geral

Desenvolver e validar uma prova de conceito (PoC) de um sistema de AIOps que integre ferramentas de monitoramento a Large Language Models (LLMs) — através de uma arquitetura flexível que suporte tanto execução local quanto consumo via API — para automatizar e enriquecer a Análise de Causa Raiz (RCA) de alertas em instâncias na nuvem.

1.1.2. Objetivos Específicos

Configurar a pilha de monitoramento baseada em ferramentas open source (Prometheus e LGTM) em ambiente de servidores cloud (AWS).

Investigar e comparar técnicas de integração entre LLMs e dados de observabilidade, bem como avaliar a viabilidade técnica de diferentes abordagens de inferência (modelos locais de menor escala versus APIs de provedores externos).

Desenvolver um middleware (script de automação em Python) capaz de interceptar alertas, extrair métricas de contexto via API e formatar as requisições para o LLM.

Implementar a técnica de injeção de contexto selecionada na etapa de pesquisa no middleware, adaptando as respostas do modelo à infraestrutura local e validando a mitigação de alucinações.

Validar a prova de conceito através da simulação de incidentes, avaliando a utilidade, precisão e latência dos diagnósticos gerados pelo sistema.