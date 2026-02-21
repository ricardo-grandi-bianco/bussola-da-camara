# Este códoigo incorpora as novas classificações manuais ao histórico (Parquet), com lógica de sobrescrita (Upsert)

# Importações
import pandas as pd
from pathlib import Path

# Configuração de caminhos
ROOT_DIR = Path(__file__).parent.parent.parent
RAW_DIR = ROOT_DIR / "data" / "raw"
PROCESSED_DIR = ROOT_DIR / "data" / "processed"

ARQUIVO_PARQUET = PROCESSED_DIR / "Votações Classificadas.parquet"
ARQUIVO_EXCEL_2026 = RAW_DIR / "votacoes_plenario_2026.xlsx"

# Baixando histórico
if ARQUIVO_PARQUET.exists():
    df_historico = pd.read_parquet(ARQUIVO_PARQUET)
    df_historico['id'] = df_historico['id'].astype(str)
else:
    df_historico = pd.DataFrame()

# Baixando novas classificações (2026)
if ARQUIVO_EXCEL_2026.exists():
    df_novos = pd.read_excel(ARQUIVO_EXCEL_2026, dtype={'id': str})
    
    # Padronização de segurança para o texto
    df_novos['classificacao'] = df_novos['classificacao'].astype(str).str.strip().str.upper()
    
    # Upsert
    df_full = pd.concat([df_historico, df_novos], ignore_index=True)
    df_final = df_full.drop_duplicates(subset='id', keep='last')

    if 'data' in df_final.columns:
        df_final = df_final.sort_values('data', ascending=False)
    
    # Salvando
    df_final.to_parquet(ARQUIVO_PARQUET, index=False)