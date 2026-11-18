# Registro de uso de IA — RotaApta

Ferramentas utilizadas: Claude Code e OpenAI Codex. A IA apoiou a preparação e a revisão do notebook, da base simulada e do script gerador. Na revisão comparativa, foram incorporadas linhas de base, uma fila de vistoria e a conferência do CSV com o gerador.

## Perguntas e orientações de trabalho

Os itens abaixo sintetizam, em forma de perguntas, os temas dos prompts usados durante o desenvolvimento e a revisão.

1. Quais são os requisitos da página 30 do PDF da FIAP e quais arquivos precisam ir para o Teams?
2. Como simular trechos urbanos sem dados pessoais e documentar a origem da base para permitir sua reprodução?
3. Como separar treino e teste e ajustar o pré-processamento somente com os dados de treino?
4. Como avaliar a previsão de tempo com MAE, RMSE e R² e a previsão de barreiras com matriz de confusão, precisão, recall e F1?
5. A regra de escolha do limiar usa só a validação cruzada do treino? Quantas barreiras ficam sem alerta e quantos falsos alertas aparecem no teste?
6. O que muda quando comparamos os modelos com referências simples, como prever tempo só pela distância ou sinalizar trechos sem rampa?
7. Com orçamento para vistoriar 20% dos trechos, quantas barreiras o ranking encontra? Como separar esse resultado simulado dos indicadores a medir no piloto?
8. Ao executar o notebook em um ambiente limpo, as métricas e os gráficos são reproduzidos? O CSV do ZIP confere com o arquivo produzido pelo gerador?

## Perguntas complementares para revisão

As perguntas a seguir detalham pontos do notebook e da comparação final.

- Quais inconsistências foram inseridas de propósito na simulação? Como a limpeza trata duplicatas, medições impossíveis e valores ausentes?
- De que forma a persistência da semente 42 ajuda a reproduzir a base? O que o SHA-256 permite conferir?
- O que muda se a divisão for feita por corredor em vez de por trecho? Em que situação isso faria diferença numa base coletada em campo?
- Qual é a diferença entre a regressão linear simples e a versão com interações? O ganho no erro de previsão justifica a perda de simplicidade?
- Qual é o papel da regularização L2 na regressão logística? Como ela afeta a interpretação dos coeficientes?
- Por que o recall medido no teste pode ficar abaixo dos 90% usados na validação para escolher o limiar?
- Como a ordem de desempate no ranking pode mudar a contagem de barreiras quando a fila tem tamanho fixo?
- O que conferir ao extrair o ZIP para que o notebook encontre o CSV e o gerador na mesma pasta?

## O que foi conferido na revisão final

- A regra do limiar seleciona a maior precisão entre as opções com recall de pelo menos 90% na validação cruzada do treino. No teste, a troca de 0,50 para aproximadamente 0,20 reduziu as barreiras sem alerta de 53 para 12 e aumentou os falsos alertas de 28 para 93.
- A fila simulada encontrou 45 barreiras em 60 vistorias. A contagem de 46 da comparação inicial veio de outra ordenação em caso de empate.
- O percentual de rotas simuladas sem barreira foi apresentado como resultado do experimento. Para o piloto, o notebook propõe medir esse indicador a partir de uma linha de base observada.
