"""
RotaApta - Gerador da base SIMULADA de trechos urbanos (RotaApta_Dataset.csv)

ORIGEM DOS DADOS: 100% simulados (sintéticos), gerados por este script com
semente fixa (reprodutível). Nenhum dado pessoal ou medição real foi utilizado.

Os parâmetros foram escolhidos para serem PLAUSÍVEIS, com base em referências
gerais de acessibilidade:
  - ABNT NBR 9050: faixa livre mínima da calçada de 1,20 m e inclinação
    máxima de rampa de 8,33% (1:12);
  - velocidade típica de deslocamento em cadeira de rodas em plano
    (ordem de grandeza ~1 m/s), reduzida por inclinação, obstáculos e
    pavimento ruim.

As relações entre variáveis foram DEFINIDAS por nós (ver fórmulas abaixo) e
acrescidas de ruído aleatório. Portanto, os modelos treinados nesta base
apenas "reencontram" essas relações: os resultados NÃO são validação em
condições reais.

Para tornar a etapa de limpeza realista, o script insere propositalmente:
valores ausentes, categorias com grafia inconsistente, valores impossíveis
(erros de digitação/sensor) e linhas duplicadas.
"""
import numpy as np
import pandas as pd

SEED = 42
N = 1500
rng = np.random.default_rng(SEED)

# ---------------------------------------------------------------- variáveis
distancia_m = np.clip(rng.lognormal(mean=np.log(180), sigma=0.55, size=N), 30, 800).round(0)
inclinacao_pct = np.clip(np.abs(rng.normal(0, 5.0, N)), 0, 16).round(1)
largura_calcada_m = np.clip(rng.normal(1.75, 0.55, N), 0.6, 3.5).round(2)

# Calçadas mais largas tendem a ter mais rampas (bairros mais estruturados)
p_rampa = 1 / (1 + np.exp(-(-1.2 + 1.0 * largura_calcada_m)))
presenca_rampa = rng.binomial(1, p_rampa)

# Calçadas estreitas concentram mais obstáculos (postes, lixeiras, degraus)
obstaculos = rng.poisson(np.clip(2.6 - 0.7 * largura_calcada_m, 0.2, None) + 0.4)
obstaculos = np.clip(obstaculos, 0, 10)

condicao_pavimento = rng.choice(["ruim", "regular", "bom"], size=N, p=[0.25, 0.45, 0.30])
efeito_pav_tempo = pd.Series(condicao_pavimento).map({"ruim": 0.30, "regular": 0.10, "bom": 0.0}).to_numpy()
efeito_pav_barr = pd.Series(condicao_pavimento).map({"ruim": 1.0, "regular": 0.35, "bom": 0.0}).to_numpy()

# ------------------------------------------------- alvo numérico: tempo (min)
# Velocidade base ~ 55 m/min (~0,9 m/s); cada fator aumenta o tempo.
velocidade_base = 55.0
tempo_min = (
    distancia_m / velocidade_base
    * (1 + 0.07 * inclinacao_pct + 0.05 * obstaculos + efeito_pav_tempo
       + 0.10 * np.clip(1.2 - largura_calcada_m, 0, None))
    + 1.2 * (1 - presenca_rampa)               # desvio / manobra sem rampa
)
# Ruído proporcional (variação entre pessoas, horário, fluxo) + pequeno ruído aditivo
tempo_min = tempo_min * rng.lognormal(0, 0.10, N) + rng.normal(0, 0.2, N)
# Limite físico: ninguém percorre o trecho a mais de ~1,5 m/s (90 m/min)
tempo_percurso_min = np.maximum(tempo_min, distancia_m / 90).round(2)

# ---------------------------------- alvo binário: barreira de acessibilidade
logit = (
    -2.6
    + 0.32 * inclinacao_pct
    - 1.6 * (largura_calcada_m - 1.2)
    + 1.3 * (1 - presenca_rampa)
    + 0.38 * obstaculos
    + efeito_pav_barr
)
p_barreira = 1 / (1 + np.exp(-logit))
barreira_acessibilidade = rng.binomial(1, p_barreira)

df = pd.DataFrame({
    "id_trecho": [f"T{i:04d}" for i in range(1, N + 1)],
    "distancia_m": distancia_m,
    "inclinacao_pct": inclinacao_pct,
    "largura_calcada_m": largura_calcada_m,
    "presenca_rampa": presenca_rampa,
    "qtd_obstaculos": obstaculos,
    "condicao_pavimento": condicao_pavimento,
    "tempo_percurso_min": tempo_percurso_min,
    "barreira_acessibilidade": barreira_acessibilidade,
})

# ------------------------------------------ "sujeira" proposital para limpeza
def sortear(frac):
    return rng.choice(N, size=int(frac * N), replace=False)

df["largura_calcada_m"] = df["largura_calcada_m"].astype(float)
df["inclinacao_pct"] = df["inclinacao_pct"].astype(float)
df["qtd_obstaculos"] = df["qtd_obstaculos"].astype(float)
df["tempo_percurso_min"] = df["tempo_percurso_min"].astype(float)

df.loc[sortear(0.03), "largura_calcada_m"] = np.nan
df.loc[sortear(0.03), "inclinacao_pct"] = np.nan
df.loc[sortear(0.02), "qtd_obstaculos"] = np.nan
df.loc[sortear(0.03), "condicao_pavimento"] = np.nan
df.loc[sortear(0.006), "tempo_percurso_min"] = np.nan          # alvo ausente

# Grafias inconsistentes
idx = sortear(0.04)
df.loc[idx, "condicao_pavimento"] = df.loc[idx, "condicao_pavimento"].map(
    {"ruim": "Ruim ", "regular": "REGULAR", "bom": " Bom"})

# Valores impossíveis (erros de cadastro/sensor)
df.loc[sortear(0.005), "largura_calcada_m"] = -1.0
df.loc[sortear(0.004), "inclinacao_pct"] = 85.0

# Duplicatas
dup = df.loc[sortear(0.01)]
df = pd.concat([df, dup], ignore_index=True).sample(frac=1, random_state=SEED).reset_index(drop=True)

if __name__ == "__main__":
    df.to_csv("RotaApta_Dataset.csv", index=False, encoding="utf-8")
    print(df.shape)
    print(df["barreira_acessibilidade"].mean().round(3))
    print(df.describe().round(2).T)
