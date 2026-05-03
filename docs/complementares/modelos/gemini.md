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

2. FUNDAMENTAÇÃO TEÓRICA

Este capítulo apresenta os conceitos estruturais necessários para a compreensão do sistema proposto. Inicialmente, discute-se a evolução do monitoramento clássico para a observabilidade em ambientes distribuídos, detalhando os tipos de dados de telemetria gerados. Em seguida, aborda-se o campo de AIOps e o uso de Modelos de Linguagem de Grande Escala (LLMs) como motores de raciocínio analítico para o diagnóstico de incidentes.

2.1 Observabilidade em Arquiteturas Nativas em Nuvem

Historicamente, o gerenciamento de infraestrutura de Tecnologia da Informação (TI) operava de maneira reativa, focado no monitoramento clássico de servidores físicos ou máquinas virtuais monolíticas. O objetivo principal era responder à pergunta binária: "O sistema está funcionando?". Contudo, a transição para arquiteturas nativas em nuvem (cloud-native), compostas por centenas de microsserviços efêmeros e contêineres, tornou essa abordagem insuficiente. Nesse novo paradigma, a pergunta fundamental mudou para: "Por que o sistema não está funcionando como deveria?" (WANG et al., 2025).

Para responder a essa questão, o conceito de Observabilidade tornou-se o padrão da indústria. Diferente do monitoramento tradicional — que se baseia em painéis de controle estáticos —, a observabilidade é a capacidade de inferir o estado interno de um sistema complexo exclusivamente a partir de suas saídas externas (telemetria).

2.1.1 Os Três Pilares da Observabilidade

Para que um sistema seja considerado "observável", ele deve exportar dados de telemetria que permitam a correlação de eventos sistêmicos. Segundo a literatura especializada (ZHANG et al., 2025), esses dados são categorizados em três pilares fundamentais:

Métricas (Metrics): São representações quantitativas do estado do sistema em um momento específico, como uso de CPU, consumo de memória ou taxa de requisições por segundo. Ferramentas como o Prometheus são otimizadas para coletar e armazenar métricas com alta eficiência temporal. Por serem dados estruturados, as métricas são ideais para disparar alertas baseados em limiares (ex: "Uso de CPU > 90%"), constituindo a etapa primária de detecção de anomalias (Failure Perception).

Logs: Consistem em registros textuais discretos e imutáveis sobre eventos que ocorreram dentro da aplicação. Ao contrário das métricas, os logs contêm contexto detalhado e frequentemente não estruturado (exceções, stack traces, mensagens de banco de dados). Ferramentas como o Loki (da pilha LGTM) agregam esses textos. O log é o principal insumo para entender o comportamento da falha.

Traces (Rastreamento Distribuído): Em um ambiente de microsserviços, uma única requisição de usuário pode passar por dezenas de serviços diferentes. O trace mapeia todo o ciclo de vida dessa requisição, permitindo identificar exatamente em qual nó da rede ocorreu a latência ou o erro.

2.1.2 O Paradoxo dos Dados e a Fadiga de Alertas

Embora a adoção de ferramentas padrão (como a pilha Prometheus e LGTM) tenha resolvido o problema da coleta de telemetria, ela introduziu um novo gargalo operacional: a explosão volumétrica de dados.

Em cenários reais de produção, uma única falha em um banco de dados pode gerar uma reação em cadeia, disparando milhares de alertas simultâneos em todos os microsserviços dependentes. Esse fenômeno, conhecido como "fadiga de alertas" (alert fatigue), sobrecarrega as equipes de Engenharia de Confiabilidade (SRE) (WANG et al., 2025). Os engenheiros são forçados a realizar a correlação manual de métricas, logs e traces espalhados por diversos dashboards para tentar encontrar a origem do problema.

Moura (2024) destaca em seu estudo que os algoritmos tradicionais de detecção são excelentes e eficientes na triagem matemática do tráfego anômalo (Métricas), mas falham gravemente em interpretar o contexto semântico do erro (Logs). Consequentemente, o Tempo Médio de Reparação (MTTR) eleva-se drasticamente não porque a falha não foi detectada, mas porque a etapa de Análise de Causa Raiz (RCA) exige um esforço cognitivo e investigativo que as ferramentas de observabilidade convencionais não conseguem fornecer.

2.1.3 Relacionamento com a Arquitetura Proposta

É exatamente nessa lacuna estrutural que a prova de conceito (PoC) deste trabalho se insere. A observabilidade moderna resolveu a etapa de Detecção com maestria matemática (via Prometheus/Alertmanager). Contudo, a etapa de Diagnóstico (RCA) continua sendo um gargalo manual.

Conforme apontado pelo survey de Zhang et al. (2025), a tentativa de usar Modelos de Linguagem para ficar lendo todo o tráfego normal em tempo real é computacional e financeiramente inviável. Portanto, justifica-se arquiteturalmente o uso das ferramentas de observabilidade clássicas como a "primeira linha de defesa" para identificar a anomalia através de regras estáticas. O LLM atua apenas de forma cirúrgica na etapa subsequente, recebendo os alertas estruturados e cruzando-os com os logs para gerar diagnósticos legíveis, mitigando o esforço cognitivo humano sem comprometer a latência da detecção inicial.