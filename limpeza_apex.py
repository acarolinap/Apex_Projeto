import fastf1
import pandas as pd
import numpy as np
import os

# Esta linha garante que a pasta de cache exista antes de habilitá-la
if not os.path.exists('cache_fastf1'):
    os.makedirs('cache_fastf1')

fastf1.Cache.enable_cache('cache_fastf1') 
# -------------------

pasta_limpa = 'apex_analytics_data_cleaned'
os.makedirs(pasta_limpa, exist_ok=True)

corridas = [
    (2024, 'Hungary'),      # Calor extremo
    (2024, 'Silverstone'),   # Clima instável
    (2024, 'Saudi Arabia'),  # Alta velocidade
    (2024, 'Monaco')         # Aceleração 0-100
]

def limpar_dados(df):
    """Função mestre de saneamento (Guia Quartz)"""
    # 1. Replace \N por nulo real
    df = df.replace(r'\\N', np.nan, regex=True)
    # 2. Garante que colunas de velocidade sejam numéricas
    cols_vel = ['Speed', 'SpeedST', 'SpeedFL']
    for col in cols_vel:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

def extrair_e_limpar_sessao(ano, local):
    print(f"\n🚀 Processando: {local} {ano}...")
    try:
        session = fastf1.get_session(ano, local, 'R')
        session.load()

        # --- TRATAMENTO DE VOLTAS (LAPS) ---
        laps = session.laps
        laps_cleaned = limpar_dados(pd.DataFrame(laps))
        # Para evitar problemas no Tableau com listas/objetos, convertemos para string
        for col in laps_cleaned.columns:
            if laps_cleaned[col].dtype == 'object':
                laps_cleaned[col] = laps_cleaned[col].astype(str)
        laps_cleaned.to_csv(f'{pasta_limpa}/{ano}_{local}_laps_cleaned.csv', index=False, encoding='utf-8-sig')

        # --- TRATAMENTO DE CLIMA (WEATHER) ---
        weather = session.weather_data
        weather_cleaned = limpar_dados(pd.DataFrame(weather))
        weather_cleaned.to_csv(f'{pasta_limpa}/{ano}_{local}_weather_cleaned.csv', index=False, encoding='utf-8-sig')

        # --- TRATAMENTO DE TELEMETRIA (FASTEST LAP) ---
        fastest = laps.pick_fastest()
        telemetry = fastest.get_telemetry()
        telemetry_cleaned = limpar_dados(pd.DataFrame(telemetry))
        
        # Filtro de Outlier Apex: Velocidades irreais
        if 'Speed' in telemetry_cleaned.columns:
            telemetry_cleaned = telemetry_cleaned[telemetry_cleaned['Speed'] <= 375]

        # 1. Salva em Parquet (Seu backup de alta performance)
        telemetry_cleaned.to_parquet(f'{pasta_limpa}/{ano}_{local}_telemetry_cleaned.parquet')
        
        # 2. CONVERSÃO PARA TABLEAU (CSV)
        # Salvamos uma cópia em CSV para o Tableau Public conseguir ler
        telemetry_cleaned.to_csv(f'{pasta_limpa}/{ano}_{local}_telemetry_tableau.csv', index=False, encoding='utf-8-sig')
        
        print(f"✅ Sucesso: {local} finalizado. Gerados Parquet e CSV para Tableau.")

    except Exception as e:
        print(f"❌ Erro em {local}: {e}")

# Execução do Pipeline
for ano, local in corridas:
    extrair_e_limpar_sessao(ano, local)

print("\n--- PIPELINE CONCLUÍDO: Agora use os arquivos .csv na pasta /" + pasta_limpa + " no Tableau ---")
