# RotaApta — Mobilidade Acessível e Inteligente

**FIAP · Global Solution 2026.2 · CitizenTech · Engenharia de Software (2º ano Fev)**

## Ficha da CitizenTech

| Campo | RotaApta |
|---|---|
| **Nome da CitizenTech** | RotaApta — Mobilidade Acessível e Inteligente |
| **Cidade e bairro** | São Paulo (SP). Bairro do piloto a definir. |
| **Cidadão beneficiado** | Pessoas com mobilidade reduzida, principalmente cadeirantes; também idosos e quem empurra carrinho de bebê. |
| **Problema, em uma frase** | Aplicativos de mapa mostram o caminho mais rápido, mas ignoram calçadas quebradas, escadas, falta de rampas e obras, e por isso pessoas com mobilidade reduzida encontram barreiras inesperadas no trajeto. |
| **Como funciona** | O usuário informa origem e destino, e o RotaApta calcula o caminho **mais acessível** (não o mais curto), considerando a condição das calçadas e rampas, os obstáculos, a distância e a dificuldade do percurso, e os relatos atualizados de outros usuários. Os próprios cidadãos informam problemas nos trajetos, mantendo os dados atualizados. |
| **O que cada parte faz** | **Frontend (React):** interface web responsiva para buscar rotas e ver alertas e níveis de risco. **Backend (Java + Spring Boot):** API REST que recebe as buscas e os relatos dos usuários. **Banco (Oracle):** armazena rotas, trechos, obstáculos e relatos. **Python, algoritmo de grafos:** calcula a rota mais adequada sobre a malha de calçadas, mesmo que seja um pouco mais longa. **Python, Data Science:** regressão linear (tempo de cada trecho) e regressão logística (probabilidade de barreira), que viram os pesos das arestas do grafo e a fila de vistoria da zeladoria. **Mapas (OpenStreetMap):** base da malha viária e de atributos como inclinação, largura, guia rebaixada e piso. |
| **Link do repositório** | https://github.com/CanaCruz/RotaApta |
| **Indicador de impacto** | % de rotas concluídas sem barreira relatada pelo usuário, medido num piloto com linha de base antes do app. Complementar: % de vistorias que encontram barreira real. |
| **ODS conectados** | **ODS 10** (meta 10.2: inclusão de pessoas com deficiência) e **ODS 11** (meta 11.2: transporte acessível; meta 11.7: espaços públicos acessíveis). |

**Resumo em uma frase:** o RotaApta transforma informações sobre barreiras urbanas em rotas mais acessíveis, ajudando pessoas com mobilidade reduzida a se deslocarem com mais independência.

## Arquitetura

| Camada | Tecnologia | Função |
|---|---|---|
| Frontend | React | Interface web responsiva (busca de rota, alertas, relato de problemas) |
| Backend | Java + Spring Boot | API REST |
| Banco de dados | Oracle | Rotas, trechos, obstáculos e relatos |
| Análise e roteamento | Python | Algoritmo de grafos + modelos estatísticos de acessibilidade |
| Mapas | OpenStreetMap | Malha viária e atributos das calçadas |

**Como o Data Science se conecta ao grafo:** cada trecho de calçada é uma aresta. O modelo de regressão linear dá o **tempo previsto** e o de regressão logística dá a **probabilidade de barreira**. Trechos acima do limiar de risco (0,20) são evitados ou penalizados, e o algoritmo de grafos procura o caminho de menor tempo entre os trechos aptos. Os relatos dos usuários e as vistorias atualizam os rótulos e permitem retreinar os modelos.

## Equipe

| Nome | RM |
|---|---|
| Arthur Canaverde da Cruz | 563029 |
| Isabella Jardim Marques | 566470 |
| Mayene Moura da Silva | 564624 |
| Murilo Canéstri dos Reis | 564053 |

## Parte de Data Science

Entrega da disciplina *Data Science & Statistical Computing* (ZIP enviado pelo Teams):

| Arquivo | Conteúdo |
|---|---|
| `RotaApta_DataScience.ipynb` | Notebook executado: análise exploratória, limpeza, divisão treino/teste sem vazamento, regressão linear (MAE, RMSE, R²), regressão logística (matriz de confusão, precisão, recall, F1), recomendações, limitações e impactos. |
| `RotaApta_Dataset.csv` | Base **simulada** de 1.515 trechos (sem dados pessoais), gerada por `gerar_dataset.py` com semente 42. |
| `gerar_dataset.py` | Gerador reprodutível da base; o notebook confere que o CSV é idêntico ao gerado. |
| `Integrantes.txt` | Nomes e RMs. |
| `prompts.md` | Registro do uso de IA (regra "IA como copiloto"). |

**Resultados principais (dados simulados, não validados em campo):**
- Tempo por trecho: MAE de 0,64 min (40% menor que usar só a distância), R² de 0,915.
- Risco de barreira: com o limiar de 0,20, o recall é de 89,5%, e as barreiras sem alerta caem de 53 para 12 em 299 trechos de teste, ao custo de 65 falsos alertas a mais.

### Como executar
Python 3.12 com `pandas==2.2.3`, `numpy==2.1.3`, `scikit-learn==1.5.2`, `matplotlib==3.9.2`, `seaborn==0.13.2` e `jupyter`. Mantenha o CSV e o `gerar_dataset.py` na mesma pasta do notebook e execute todas as células em ordem.

## Uso de IA
Ferramentas: Claude Code (Anthropic) e OpenAI Codex, como copilotos. Os prompts estão registrados em `prompts.md`, e cada integrante deve saber explicar o código.
