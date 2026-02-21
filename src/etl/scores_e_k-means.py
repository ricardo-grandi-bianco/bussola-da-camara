# Este código processa os scores de cada deputado e executa o k-means

# Importações
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from pathlib import Path

# Configuração de caminhos
ROOT_DIR = Path(__file__).parent.parent.parent
PROCESSED_DIR = ROOT_DIR / "data" / "processed"
FINAL_DIR = ROOT_DIR / "data" / "final"

# Lendo arquivos
df_classificacao = pd.read_parquet(PROCESSED_DIR / "Votações Classificadas.parquet")
df_votacoes = pd.read_parquet(PROCESSED_DIR / "Matriz Votos.parquet")

# Parte 1: calculando e atribuindo o score de cada deputado

# Preparação dos metadados
df_classificacao['id'] = df_classificacao['id'].astype(str)
mapa_classificacao = df_classificacao.set_index('id')['classificacao'].to_dict()
cols_meta = ['deputado_id', 'deputado_nome', 'deputado_siglaPartido', 'deputado_siglaUf', 'deputado_urlFoto']
cols_votos = [c for c in df_votacoes.columns if c not in cols_meta]

dict_scores_x = {}
dict_scores_y = {}

# Loop principal, que calcula o score base, ignora os projetos inclassificáveis (I) e desconsidera, por ora, os moderados (M)

for votacao_id in cols_votos:

    # Verificando a classificação da votação (se for direita, esquerda, conservador ou progressista, mantém)
    tipo_projeto = mapa_classificacao.get(votacao_id)
    if tipo_projeto not in ['D', 'E', 'C', 'P']:
        continue

    # Extraindo a série de votos
    coluna_votos = df_votacoes[votacao_id]
    votos_validos = coluna_votos.dropna()

    if len(votos_validos) == 0:
        continue # Evita divisão por zero
    
    # Calcula as proporções e os pesos de cada votação
    total = len(votos_validos)
    qtd_sim = (votos_validos == 1).sum()
    qtd_nao = (votos_validos == -1).sum()
    prop_sim = qtd_sim / total
    prop_nao = qtd_nao / total
    
    peso_sim_absoluto = (1 - prop_sim) * 10
    peso_nao_absoluto = (1 - prop_nao) * 10
    
    score_sim = 0
    score_nao = 0
    destino = None

    # Determina o eixo (economia ou outros temas) e o sinal (+ para direita ou conservador, - para esquerda ou progressista)
    if tipo_projeto == 'E':
        score_sim = -1 * peso_sim_absoluto
        score_nao = +1 * peso_nao_absoluto
        destino = dict_scores_x

    elif tipo_projeto == 'D':
        score_sim = +1 * peso_sim_absoluto
        score_nao = -1 * peso_nao_absoluto
        destino = dict_scores_x

    elif tipo_projeto == 'P':
        score_sim = -1 * peso_sim_absoluto
        score_nao = +1 * peso_nao_absoluto
        destino = dict_scores_y

    elif tipo_projeto == 'C':
        score_sim = +1 * peso_sim_absoluto
        score_nao = -1 * peso_nao_absoluto
        destino = dict_scores_y

    # Mapeando votos -1 e 1 para o score (NaN não entra)
    if destino is not None:
        series_score = coluna_votos.map({1: score_sim, -1: score_nao})
        destino[votacao_id] = series_score

# Consolidação
df_scores_x = pd.DataFrame(dict_scores_x, index=df_votacoes.index)
df_scores_y = pd.DataFrame(dict_scores_y, index=df_votacoes.index)
df_votacoes['score_base_x'] = df_scores_x.mean(axis=1)
df_votacoes['score_base_y'] = df_scores_y.mean(axis=1)

# Pós-processamento para incluir votações classificadas como M (moderadas)

# Preparação dos metadados
cols_base_x = [col for col, tipo in mapa_classificacao.items() if tipo in ['D', 'E'] and col in df_votacoes.columns]

cols_M = [col for col, tipo in mapa_classificacao.items() if tipo == 'M' and col in df_votacoes.columns]

print(f"Votações Base (D/E): {len(cols_base_x)}")
print(f"Votações Moderadas (M): {len(cols_M)}")

# Contando votos válidos na base (necessário para a média ponderada) e calculando notas M por votação
contagem_votos_base = df_votacoes[cols_base_x].count(axis=1)
dict_scores_M_individuais = {}

for votacao_id in cols_M:
    coluna_votos = df_votacoes[votacao_id]
    votos_validos = coluna_votos.dropna()

    if len(votos_validos) == 0:
        continue

    indices_sim = votos_validos[votos_validos == 1].index
    indices_nao = votos_validos[votos_validos == -1].index

    if len(indices_sim) == 0 or len(indices_nao) == 0:
        continue

    # Teste de centralidade (extremos vs centro)
    media_abs_sim = df_votacoes.loc[indices_sim, 'score_base_x'].abs().mean()
    media_abs_nao = df_votacoes.loc[indices_nao, 'score_base_x'].abs().mean()

    if media_abs_sim > media_abs_nao:
        grupo_extremo = indices_sim
        grupo_centro = indices_nao
    else:
        grupo_extremo = indices_nao
        grupo_centro = indices_sim

    # Calculando os scores de cada voto
    total = len(votos_validos)
    prop_extremo = len(grupo_extremo) / total
    valor_escassez = (1 - prop_extremo) * 10
    
    scores_atuais = df_votacoes.loc[grupo_extremo, 'score_base_x']
    sinais = np.sign(scores_atuais)
    
    notas_extremo = sinais * valor_escassez
    notas_centro = pd.Series(0.0, index=grupo_centro)
    
    notas_projeto = pd.concat([notas_extremo, notas_centro])
    dict_scores_M_individuais[votacao_id] = notas_projeto

# Consolidação e cálculo da nova média (score_pos_x)
df_scores_M = pd.DataFrame(dict_scores_M_individuais)
soma_notas_M = df_scores_M.sum(axis=1).fillna(0)
contagem_votos_M = df_scores_M.count(axis=1).fillna(0)

numerador = (df_votacoes['score_base_x'].fillna(0) * contagem_votos_base) + soma_notas_M
denominador = contagem_votos_base + contagem_votos_M
df_votacoes['score_pos_x'] = numerador / denominador.replace(0, np.nan)

# Comparativo para ver quem se moveu mais
df_votacoes['delta_real'] = df_votacoes['score_pos_x'] - df_votacoes['score_base_x']

# Normalização de escala (-10 a 10)
max_x_atual = df_votacoes['score_pos_x'].abs().max()
max_y_atual = df_votacoes['score_base_y'].abs().max() 
fator_x = 10 / max_x_atual
fator_y = 10 / max_y_atual

df_votacoes['x_final'] = df_votacoes['score_pos_x'] * fator_x
df_votacoes['y_final'] = df_votacoes['score_base_y'] * fator_y

# Parte 2: treinando o K-means (k=7)

# Preparação da matriz
cols_meta = [
    'deputado_id', 'deputado_nome', 'deputado_siglaPartido',
    'deputado_siglaUf', 'deputado_urlFoto',
    'score_base_x', 'score_base_y', 'score_pos_x', 'delta_real',
    'x_final', 'y_final'
]
cols_votos = [c for c in df_votacoes.columns if c not in cols_meta]
X_kmeans = df_votacoes[cols_votos].fillna(0)

# Execução do modelo
kmeans7 = KMeans(n_clusters=7, init='k-means++', n_init=20, random_state=42)
df_votacoes['cluster_7'] = kmeans7.fit_predict(X_kmeans).astype(str)

# Salvando os arquivos finais (sobrescritos)
cols_essenciais = [
    'deputado_id',           
    'deputado_nome',        
    'deputado_siglaPartido', 
    'deputado_siglaUf',      
    'deputado_urlFoto',      
    'x_final',               
    'y_final',               
    'cluster_7',            
    'delta_real'            
]

cols_existentes = [c for c in cols_essenciais if c in df_votacoes.columns]
df_dash = df_votacoes[cols_existentes].copy()
df_dash = df_dash.rename(columns={'cluster_7': 'cluster'})

df_votacoes.to_parquet(PROCESSED_DIR / "bussola_completa.parquet", index=False)
df_dash.to_parquet(FINAL_DIR / "bussola_dash_producao.parquet", index=False)
