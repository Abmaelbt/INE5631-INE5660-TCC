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

Historicamente, o gerenciamento de infraestrutura de Tecnologia da Informação (TI) operava de maneira reativa, focado no monitoramento clássico de servidores físicos ou máquinas virtuais monolíticas. O objetivo principal era responder à pergunta binária: "O sistema está funcionando?". Contudo, a transição para arquiteturas nativas em nuvem (cloud-native), compostas por centenas de microsserviços efêmeros e contêineres, tornou essa abordagem insuficiente. Nesse novo paradigma, a complexidade arquitetural exige que a pergunta mude para: "Por que o sistema não está funcionando como deveria?" (WANG et al., 2025; BEYER et al., 2016).

Para responder a essa questão, o conceito de Observabilidade tornou-se o padrão da indústria. Diferente do monitoramento tradicional — que se baseia em painéis de controle estáticos predefinidos —, a observabilidade, termo emprestado da teoria de controle, é a capacidade de inferir o estado interno de um sistema complexo exclusivamente a partir do conhecimento de suas saídas externas, ou seja, de sua telemetria (NIEDERMAYR et al., 2019).

2.1.1 Os Três Pilares da Observabilidade

Para que um sistema seja considerado "observável", ele deve exportar dados de telemetria estruturados que permitam a correlação de eventos sistêmicos. A literatura especializada e as práticas de Engenharia de Confiabilidade de Sites (SRE) consolidaram esses dados em três pilares fundamentais (ZHANG et al., 2025):

Métricas (Metrics): São representações quantitativas do estado do sistema agregadas em intervalos de tempo, como uso de CPU, consumo de memória ou taxa de requisições por segundo. Ferramentas como o Prometheus são otimizadas para coletar e armazenar métricas com alta eficiência, sendo ideais para disparar alertas baseados em limiares e constituindo a etapa primária de detecção de anomalias (Failure Perception) (TURNBULL, 2018).

Logs: Consistem em registros textuais discretos e imutáveis sobre eventos que ocorreram dentro da aplicação. Ao contrário das métricas, os logs contêm contexto detalhado e frequentemente não estruturado (exceções, stack traces, mensagens de banco de dados). O log atua como o principal insumo investigativo para entender a natureza comportamental da falha (MOURA, 2024).

Traces (Rastreamento Distribuído): Em um ecossistema de microsserviços, o ciclo de vida de uma única requisição de usuário frequentemente transita por dezenas de serviços diferentes. O trace (como implementado no sistema Dapper do Google) mapeia essa trajetória, permitindo identificar o nó exato da rede responsável pela latência ou erro em cadeias de dependência complexas (SIGELMAN et al., 2010).

A Tabela 1 sintetiza as características fundamentais de cada pilar da observabilidade, destacando suas estruturas de dados e a respectiva finalidade operacional no contexto deste trabalho.

Tabela 1 – Síntese dos Três Pilares da Observabilidade
![alt text](image.png)

Fonte: Autoria própria (2026).

2.1.2 O Paradoxo dos Dados e a Fadiga de Alertas

A adoção do padrão de observabilidade e de ecossistemas maduros, como a pilha LGTM (Loki, Grafana, Tempo, Mimir), solucionou o desafio da coleta de telemetria, mas introduziu um novo gargalo operacional: a explosão volumétrica de dados.

Em cenários produtivos reais, uma única falha em um componente basilar (como um banco de dados) deflagra uma cascata de falhas de conectividade, disparando milhares de notificações simultâneas em todos os microsserviços dependentes. Esse fenômeno, cunhado como "fadiga de alertas" (alert fatigue), deteriora a capacidade de resposta das equipes de operações, que perdem tempo crítico tentando correlacionar manualmente os sinais vitais espalhados por diversos painéis de controle (WANG et al., 2025).

A deficiência reside no fato de que os sistemas tradicionais de alerta são estritamente matemáticos. Eles são eficientes na detecção inicial baseada em limiares (métricas), porém falham gravemente na interpretação do contexto semântico da ocorrência. Como resultado, a Análise de Causa Raiz (RCA) converte-se em um extenuante exercício de correlação humana (MOURA, 2024), elevando drasticamente o Tempo Médio de Reparação (MTTR).

(INSERIR AQUI A FIGURA 1 CRIADA NO DRAW.IO - ILUSTRANDO A CASCATA DE FALHAS)

2.1.3 Relacionamento com a Arquitetura Proposta

É precisamente nesta lacuna arquitetural que a prova de conceito (PoC) desenvolvida neste trabalho se insere. A observabilidade clássica solucionou a etapa de Detecção com alta performance e baixo custo computacional (via Prometheus e Alertmanager). No entanto, o Diagnóstico (RCA) permanece como o gargalo dependente de esforço cognitivo.

Tentativas de empregar Inteligência Artificial para substituir todo o pipeline de monitoramento, analisando o tráfego normal em tempo real, mostram-se financeiramente proibitivas e ineficientes devido à latência de inferência (ZHANG et al., 2025). Dessa forma, a arquitetura proposta sustenta o paradigma híbrido: mantém as ferramentas de observabilidade determinísticas como a linha de frente para a triagem primária da anomalia e aciona as capacidades de raciocínio lógico dos Modelos de Linguagem (LLMs) exclusivamente na etapa investigativa do RCA. Nesta fase, o sistema injeta os alertas e o contexto dos logs no modelo, delegando a correlação de dados complexos para gerar um diagnóstico sintético e imediatamente acionável.

2.2 Inteligência Artificial para Operações de TI (AIOps)

Com a explosão volumétrica de dados gerados pelos pilares da observabilidade, a dependência exclusiva da análise humana tornou-se o principal gargalo para a garantia de disponibilidade dos serviços. Para mitigar esse problema, a indústria cunhou o termo AIOps (Artificial Intelligence for IT Operations), introduzido pelo Gartner em 2016, que designa a aplicação de técnicas de Machine Learning (ML) para automatizar a detecção, o diagnóstico e a resolução de incidentes.

2.2.1 As Limitações do AIOps Tradicional

A primeira geração de ferramentas de AIOps baseava-se estritamente em algoritmos clássicos de aprendizado de máquina. Embora eficientes na identificação de desvios matemáticos em séries temporais (anomalias em métricas), essas abordagens esbarraram em limitações severas quando aplicadas a ambientes de produção dinâmicos:

A Caixa Preta do Diagnóstico: A maior falha do ML clássico no contexto de operações é a incapacidade de explicar seus resultados. O modelo aponta a anomalia matemática, mas não fornece uma narrativa compreensível sobre as correlações causais.

Falta de Generalização: Um modelo treinado para identificar falhas em um serviço perdia sua eficácia (concept drift) assim que o código sofria uma atualização, exigindo retreinamentos constantes e custosos.

Incapacidade Semântica: Modelos tradicionais não compreendem texto bruto nativamente. A extração de informações de logs exigia complexos pipelines de log parsing baseados em expressões regulares, que quebravam constantemente (MOURA, 2024).

2.2.2 A Evolução com Modelos de Linguagem de Grande Escala (LLMs)

A introdução de Modelos de Linguagem de Grande Escala (LLMs) redefiniu as capacidades do AIOps, preenchendo a principal lacuna deixada pelo ML tradicional: a interpretação semântica de logs e traces (ZHANG et al., 2025).

Diferente de modelos restritos a uma única tarefa matemática, os LLMs são redes neurais baseadas na arquitetura Transformer, pré-treinadas em vastos volumes de dados textuais — incluindo código-fonte, manuais de infraestrutura e fóruns de discussão de TI. Isso lhes confere uma capacidade ímpar de correlacionar anomalias de infraestrutura com explicações legíveis em linguagem natural.

A aplicação pragmática dessas ferramentas no contexto operacional moderno não exige o retreinamento do modelo do zero, baseando-se em técnicas de inferência direcionada:

Aprendizado em Contexto (In-Context Learning - ICL): É a capacidade do LLM de adaptar-se a uma tarefa baseando-se exclusivamente nas instruções e exemplos fornecidos no prompt no momento da requisição. Essa técnica elimina a dependência de ciclos de fine-tuning e permite que o modelo interprete formatos de logs proprietários dinamicamente.

Raciocínio em Cadeia (Chain-of-Thought - CoT): Técnica de estruturação de prompt que força a inteligência artificial a decompor o processo investigativo em etapas lógicas e explícitas (ex: "1. Avalie a métrica -> 2. Busque o erro no log -> 3. Sugira a causa"). Segundo Wang et al. (2025), o uso de CoT no cruzamento de dados de telemetria reduz drasticamente o risco de "alucinações" nos diagnósticos.

2.2.3 O Paradigma Híbrido: Detecção vs. Interpretação

Apesar de suas notáveis capacidades na Análise de Causa Raiz (RCA), o uso operacional de LLMs introduz desafios estruturais. Devido à sua natureza arquitetural, LLMs possuem alta latência de inferência e custo computacional substancial. Portanto, a literatura técnica condena o uso dessas redes para monitoramento contínuo em tempo real (ZHANG et al., 2025).

A resposta da indústria a esse desafio — e que fundamenta a arquitetura proposta neste trabalho — é a consolidação de um paradigma híbrido. Ferramentas determinísticas de observabilidade (como o Prometheus) são mantidas na linha de frente para a fase de Detecção (Failure Perception), operando de forma barata e em milissegundos. O acionamento do LLM ocorre apenas de forma reativa, atuando exclusivamente na fase de RCA. Nessa etapa, a IA recebe o alerta estruturado e os logs filtrados da janela de tempo da falha, utilizando sua capacidade semântica para gerar o diagnóstico final sem sobrecarregar a infraestrutura de monitoramento.

2.3 Large Language Models (LLMs) em Operações

A transição de algoritmos estatísticos puros para Modelos de Linguagem de Grande Escala (LLMs) representa o atual estado da arte no campo de AIOps. Diferente dos sistemas de Machine Learning tradicionais, que exigiam rigorosa engenharia de características (feature engineering) para converter logs textuais em matrizes numéricas, os LLMs atuam como motores de raciocínio cognitivo, capazes de interpretar o jargão técnico, arquiteturas de infraestrutura e mensagens de erro nativamente em linguagem natural (AHMED et al., 2023).

2.3.1 Arquitetura Transformer e o Ecossistema de LLMs

A capacidade interpretativa dos LLMs advém de sua arquitetura base, o Transformer, especificamente de sua topologia baseada apenas em decodificadores (Decoder-only). O mecanismo de "Atenção Plena" (Self-Attention) inerente a essa arquitetura permite que o modelo pondere a relevância de diferentes palavras e símbolos em uma longa sequência de texto. No contexto de observabilidade, isso significa que a IA consegue relacionar uma métrica de CPU_Usage no início de um alerta com uma exceção de banco de dados (TimeoutException) dezenas de linhas abaixo em um arquivo de log, extraindo a correlação causal.

A adoção destas ferramentas na resolução de incidentes divide-se atualmente em dois paradigmas principais de inferência, cada um com trade-offs específicos para ambientes corporativos corporativos (ZHANG et al., 2024):

Modelos Comerciais (APIs de Nuvem): Soluções fechadas (closed-source), como o GPT-4o (OpenAI) e Gemini (Google), que rodam em infraestruturas de hiperescala e contam com centenas de bilhões de parâmetros. Oferecem capacidade de raciocínio incomparável e baixa fricção de desenvolvimento. No entanto, exigem o envio de dados telemétricos (frequentemente contendo IPs, credenciais mascaradas e arquiteturas internas) para servidores de terceiros, esbarrando em rígidas políticas de conformidade e privacidade (LGPD/GDPR), além de gerarem custos recorrentes por token analisado.

Modelos Open-Source Locais: Modelos de pesos abertos, como Llama 3 (Meta) e Qwen 2.5 (Alibaba), projetados para serem hospedados internamente pela própria organização. Para viabilizar a execução em hardware comercial restrito sem o uso de supercomputadores, esses modelos passam por processos de quantização (redução da precisão matemática de seus pesos para formatos como 4-bit ou 8-bit). Embora mitiguem completamente o risco de vazamento de dados corporativos (data privacy) e eliminem o custo de APIs comerciais, modelos menores (na faixa de 3 a 8 bilhões de parâmetros) exigem técnicas rigorosas de injeção de contexto para não perderem a precisão diagnóstica em cenários complexos.

2.3.2 Limitações e Desafios: Alucinações e Latência

Apesar do notável desempenho na automação do RCA, a aplicação de LLMs em sistemas críticos de infraestrutura enfrenta obstáculos técnicos severos. O principal deles é o fenômeno da Alucinação, onde o modelo gera saídas sintaticamente fluentes, porém factualmente incorretas.

No domínio de Operações de TI, uma alucinação não é apenas um erro de cálculo; é um risco de integridade. Um modelo pode diagnosticar incorretamente a queda de um serviço inexistente ou, em cenários de auto-remediação (self-healing), sugerir e executar scripts bash destrutivos na produção. Para mitigar esse risco, a validação de LLMs em AIOps tem adotado práticas de Engenharia do Caos (Chaos Engineering). Szandała (2025) propõe que a eficácia diagnóstica de um LLM só deve ser validada submetendo-o a falhas intencionais injetadas em ambientes controlados, medindo sua aderência à verdade estrutural do sistema em vez de confiar cegamente na fluência textual gerada.

Adicionalmente, a latência de inferência impõe restrições ao monitoramento contínuo. Mesmo com aceleração via GPU, a geração autointeligente de relatórios (token por token) possui um atraso inerente. Por isso, reitera-se a necessidade do paradigma híbrido: o LLM não deve ser utilizado como ferramenta de percepção em tempo real, mas invocado sob demanda apenas após o disparo de um alerta de ferramentas determinísticas tradicionais.

2.3.3 A Janela de Contexto em Logs

Uma limitação arquitetural intrínseca dos LLMs é a Janela de Contexto (Context Window), que define a quantidade máxima de tokens (fragmentos de palavras e código) que o modelo consegue processar simultaneamente em uma única requisição.

Os logs de infraestrutura e aplicação, por natureza, são extremamente verbosos, repetitivos e carregados de ruído temporal (como timestamps milissegundos e hashes de sessão). Zhou et al. (2026) destacam que injetar despejos brutos de logs diretamente no prompt do LLM frequentemente extrapola o limite de contexto. Além disso, mesmo quando o limite não é ultrapassado, modelos tendem a sofrer do efeito "Lost in the Middle" (Perdido no Meio), onde informações cruciais sobre a causa raiz localizadas no centro de um log longo são ignoradas em prol de anomalias triviais no início ou no fim do documento.

Para viabilizar o RCA automatizado, torna-se obrigatória a construção de um middleware que aplique a poda sintática de logs — filtrando linhas informacionais (INFO) e removendo timestamps redundantes — antes de encaminhar a carga útil (payload) estruturada para o modelo de linguagem. É essa curadoria da janela de contexto que garante diagnósticos precisos tanto em modelos comerciais quanto em arquiteturas open-source restritas.