# 2.2 AIOps e Modelos de Linguagem

## 2.2.1 Definição e Evolução do AIOps
A complexidade das infraestruturas de TI modernas impulsionou a necessidade de automação cognitiva. O termo AIOps (*Artificial Intelligence for IT Operations*), consolidado inicialmente pelo Gartner, refere-se à aplicação de aprendizado de máquina (*Machine Learning*), ciência de dados e análises avançadas para aprimorar, diagnosticar e automatizar operações de TI [prasad2018market]. 
O objetivo principal das plataformas de AIOps clássicas é romper com os silos operacionais e agregar grandes volumes de dados (telemetria) de múltiplas fontes, reduzindo o ruído dos alertas por meio da correlação estatística para prever interrupções de serviço.

## 2.2.2 As Limitações do AIOps Clássico e o Obstáculo Semântico
Durante a primeira onda do AIOps (pré-IA Generativa), a indústria focou-se no emprego de algoritmos tradicionais, como detecção de anomalias estatísticas, agrupamento espacial (*clustering*) e árvores de decisão. 
Apesar de extremamente eficientes na análise do comportamento quantitativo (Métricas) — como a identificação em tempo real de que um servidor excedeu o desvio padrão histórico de consumo de CPU —, esses métodos são desprovidos de capacidade semântica [moura2024deteccao]. 
Isso significa que as soluções de AIOps tradicionais apontam *quando* e *onde* a anomalia começou, mas esbarram em uma limitação técnica profunda ao tentar processar e interpretar a natureza textual dos *logs* de erro. Consequentemente, a etapa decisiva da Análise de Causa Raiz (RCA) exigia que um engenheiro humano realizasse a "leitura" do erro propriamente dito.

## 2.2.3 A Ascensão dos LLMs em Operações de Confiabilidade (SRE)
O surgimento e a democratização dos Modelos de Linguagem de Grande Escala (LLMs) modificaram profundamente a forma com a qual o RCA pode ser solucionado [survey_llm_aiops_2024].
Por serem fundamentalmente construídos para processamento de linguagem natural (NLP) e treinados em vastos repositórios de código e fóruns técnicos, os LLMs conseguem inferir regras, interpretar exceções obscuras e entender *stack traces* nativamente, sem a necessidade de pré-processamento extenuante ou regras estáticas [wang_2025_integrating].
Nesse paradigma, o modelo assume o papel de um assistente de engenharia cognitiva. Ao receber os relatórios textuais do sistema, a IA Generativa é capaz de traçar a narrativa do incidente, identificando, por exemplo, que a sobrecarga do banco de dados originou-se de uma falha crônica de autenticação num \textit{token} mal configurado.

## 2.2.4 Arquiteturas Práticas: Injeção de Contexto e Mitigação de Alucinações
Apesar da altíssima capacidade analítica, LLMs de fundação — como Llama 3, GPT-4, Groq ou Gemini — sofrem de um viés intrínseco: eles desconhecem a arquitetura topológica interna da organização. Como o modelo não foi treinado com os códigos e a infraestrutura privada da empresa, ele não possui contexto natural para diagnosticar serviços com nomes internos (ex: o que faz o servidor `wplexep`).
Esse isolamento induz ao risco crítico da "Alucinação" computacional, onde a IA preenche lacunas de conhecimento com explicações plausíveis, porém factualmente incorretas.

Para sobrepor esse viés e viabilizar a implementação deste trabalho, a literatura recente prescreve a utilização de arquiteturas baseadas em RAG (*Retrieval-Augmented Generation*) ou Injeção Extensa de Contexto (*In-Context Learning*) [survey_llm_aiops_2024]. 
O funcionamento arquitetural proposto no protótipo inverte o fluxo passivo: o *middleware* em Python capta os alertas matemáticos das ferramentas clássicas de AIOps (Prometheus), e atua como o **recuperador de informações**, buscando no banco de *logs* (Loki) todos os rastros deixados pela falha num intervalo definido de minutos. Em seguida, os *logs* estruturados são injetados diretamente no *prompt* restritivo do modelo LLM. Ao saturar o LLM com contexto recente e forçar que a resposta se limite aos fatos relatados pelos *logs* fornecidos, a probabilidade de alucinações é mitigada, resultando na extração precisa e confiável da Causa Raiz do incidente.
