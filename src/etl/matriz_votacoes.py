# Este código gera a matriz de votações, utilizada para calcular os scores dos deputados e treinar o K-means

# Importações
import pandas as pd
import numpy as np
from pathlib import Path

# Configuração de caminhos
ROOT_DIR = Path(__file__).parent.parent.parent 
DATA_PROCESSED = ROOT_DIR / "data" / "processed"


# Baixando e lendos dados das votações individuais da API da Câmara
dados2023 = "http://dadosabertos.camara.leg.br/arquivos/votacoesVotos/csv/votacoesVotos-2023.csv"
dados2024 = "http://dadosabertos.camara.leg.br/arquivos/votacoesVotos/csv/votacoesVotos-2024.csv"
dados2025 = "http://dadosabertos.camara.leg.br/arquivos/votacoesVotos/csv/votacoesVotos-2025.csv"
dados2026 = "http://dadosabertos.camara.leg.br/arquivos/votacoesVotos/csv/votacoesVotos-2026.csv"
df2023 = pd.read_csv(dados2023, sep = ";", encoding = "latin1")
df2024 = pd.read_csv(dados2024, sep = ";", encoding = "latin1")
df2025 = pd.read_csv(dados2025, sep = ";", encoding = "latin1")
df2026 = pd.read_csv(dados2026, sep = ";", encoding = "latin1")

# Unindo os dfs e excluindo colunas irrelevantes
df_bruto = pd.concat([df2023, df2024, df2025, df2026])
df_bruto = df_bruto.drop(columns=['uriVotacao','dataHoraVoto', 'deputado_uri', 'deputado_uriPartido', 'deputado_idLegislatura'])

# Baixando votações classificadas
df_class = pd.read_parquet(DATA_PROCESSED / "Votações Classificadas.parquet")

# Tratamento preliminar
df_bruto = df_bruto.rename(columns={'ï»¿"idVotacao"': 'id_votacao'}) 
df_class['id'] = df_class['id'].astype(str)
df_bruto['id_votacao'] = df_bruto['id_votacao'].astype(str)

# Mantendo no df_bruto apenas as votações já classificadas
ids_classificados = df_class['id'].unique()
df_bruto_filtrado = df_bruto[df_bruto['id_votacao'].isin(ids_classificados)]

# Pivotagem
df_votos = df_bruto_filtrado.pivot_table(
    index=['deputado_id', 'deputado_nome', 'deputado_siglaPartido', 'deputado_siglaUf', 'deputado_urlFoto'],
    columns='id_votacao',
    values='voto',
    aggfunc='first'
).reset_index()
df_votos.columns.name = None

# Transformando os votos em dados numéricos (lidando com erros de encoding, quando necessário)
mapa_votos = {
    'Sim': 1,

    'Não': -1,
    'NÃ£o': -1,          
    'Nao': -1,           

    'Obstrução': -1,
    'ObstruÃ§Ã£o': -1,   
    'Obstrucao': -1,

    'Abstenção': np.nan,
    'AbstenÃ§Ã£o': np.nan,
    'Abstencao': np.nan,
    'Artigo 17': np.nan,
    'Art. 17': np.nan,
    '-': np.nan          
}

colunas_info = ['deputado_id', 'deputado_nome', 'deputado_siglaPartido', 'deputado_siglaUf', 'deputado_urlFoto']
colunas_votacao = [c for c in df_votos.columns if c not in colunas_info]
df_numerico = df_votos.copy()
for col in colunas_votacao:
    df_numerico[col] = df_numerico[col].map(mapa_votos)
df_numerico = df_numerico.dropna(subset=colunas_votacao, how='all')

# Correção de nomes (encoding)
def corrigir_mojibake(texto):
    if not isinstance(texto, str):
        return texto
    try:
        return texto.encode('latin1').decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return texto

df_numerico['deputado_nome'] = df_numerico['deputado_nome'].apply(corrigir_mojibake)

# Filtro de presença (40%)
pct_minimo = 0.40
limite_votos = int(len(colunas_votacao) * pct_minimo)
df_final = df_numerico.dropna(subset=colunas_votacao, thresh=limite_votos).copy()

# Salvando o arquivo em parquet (sobrescrito)
df_final.to_parquet(DATA_PROCESSED / "Matriz Votos.parquet", index=False)
