# Registro de uso de IA — RotaApta (Data Science)

Conforme a regra "IA como copiloto" da GS 2026.2: a IA foi usada para apoiar a construção do notebook. A equipe revisou o código e deve saber explicar cada linha.

- **Ferramenta:** Claude Code (Anthropic), modelo Claude Opus 5.5
- **Data:** 12/11/2026
- **Arquivos gerados com apoio da IA:** `RotaApta_DataScience.ipynb`, `RotaApta_Dataset.csv`, `gerar_dataset.py`, este `prompts.md`
- **Também usado:** OpenAI Codex, que produziu uma versão alternativa; ideias dela foram incorporadas após revisão comparativa (ver item 5)

## Prompts utilizados

### 1. Pedido inicial (enunciado do trabalho)
> Preciso desenvolver a entrega completa da disciplina Data Science & Statistical Computing, seguindo os requisitos da página 30 do PDF da FIAP. [...] O RotaApta é uma plataforma web que ajuda pessoas com mobilidade reduzida, principalmente cadeirantes, a encontrar rotas urbanas acessíveis [...] Criar ou utilizar uma base CSV com informações de trechos urbanos [...] Modelo 1 — Regressão Linear [...] MAE, RMSE, R² [...] Modelo 2 — Regressão Logística [...] matriz de confusão, precisão, recall, F1-score [...] Não inventar resultados de avaliação: executar os modelos e apresentar as métricas calculadas.
>
> ve se da pra entedner oq tem q ser feito

### 2. Envio do PDF da atividade
> segue pdf *(arquivo "GS CitizenTech - 2ES Fev - FIAP 2026.pdf")*

### 3. Autorização para desenvolver
> Sim, pode instalar o Python 3.12 e começar o desenvolvimento completo do Data Science do RotaApta. Prefiro que você execute tudo localmente para garantir que o notebook funcione corretamente e que as métricas sejam calculadas de verdade. [...] Utilize dados simulados plausíveis, identificando claramente sua origem. Inclua as hipóteses, os ODS 10 e 11 e o arquivo `prompts.md`. [...] Importante: não considere uma hipótese comprovada apenas pelo coeficiente de um modelo treinado com dados simulados. Explique as limitações dos resultados.

### 4. Revisão comparativa
> Quero que você faça uma revisão comparativa de duas entregas de Data Science do RotaApta para a FIAP: a versão que você criou e a versão do Codex [...] Use a página 30 do PDF como rubrica [...]

### 5. Aplicação das correções da revisão
> Sim, aplicar C1–C6

Correções aplicadas: integrantes preenchidos; impacto simulado deixou de ser apresentado como meta; nota sobre a regularização L2 da regressão logística; linhas de base "somente distância" e "regra sem rampa"; fila de vistoria com orçamento de 20%; conferência do CSV contra o gerador. As linhas de base, a fila de vistoria e a conferência do CSV foram inspiradas na versão produzida com o OpenAI Codex.

## Decisões tomadas pela IA e revisadas pela equipe
- Dados **simulados** (sem dados pessoais), com gerador reprodutível (`gerar_dataset.py`, semente 42) e parâmetros inspirados na NBR 9050.
- Sujeira proposital na base (ausentes, duplicatas, grafias, valores impossíveis) para demonstrar a limpeza.
- Pré-processamento dentro de `Pipeline` (ajustado só no treino); um alvo nunca usado como entrada do outro modelo.
- Limiar da regressão logística escolhido no treino (validação cruzada) priorizando o recall.
- Hipóteses tratadas como "compatíveis com os dados simulados", nunca como "comprovadas".

## O que cada integrante deve saber explicar
1. Por que os dados são simulados e o que isso significa para os resultados.
2. Por que a imputação e a padronização ficam dentro do `Pipeline` (vazamento de dados).
3. O que significam MAE, RMSE e R², e os números obtidos.
4. A matriz de confusão e por que escolhemos o limiar de 0,20 (recall acima de precisão).
5. Como as previsões viram recomendação de rota e priorização de reparos.
