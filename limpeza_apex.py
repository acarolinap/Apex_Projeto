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
    (2024, 'Hungary'),      # Calor extremo (Pergunta 3)
    (2024, 'Silverstone'),   # Clima instável (Pergunta 1 e 3)
    (2024, 'Saudi Arabia'),  # Alta velocidade (Pergunta 2)
    (2024, 'Monaco')         # Aceleração 0-100 (Pergunta 4)
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
        # Salva o CSV limpo
        laps_cleaned.to_csv(f'{pasta_limpa}/{ano}_{local}_laps_cleaned.csv', index=False)

        # --- TRATAMENTO DE CLIMA (WEATHER) ---
        weather = session.weather_data
        weather_cleaned = limpar_dados(pd.DataFrame(weather))
        weather_cleaned.to_csv(f'{pasta_limpa}/{ano}_{local}_weather_cleaned.csv', index=False)

        # --- TRATAMENTO DE TELEMETRIA (FASTEST LAP) ---
        # Pegamos a volta mais rápida para análise de performance pura (Pergunta 2)
        fastest = laps.pick_fastest()
        telemetry = fastest.get_telemetry()
        telemetry_cleaned = limpar_dados(pd.DataFrame(telemetry))
        
        # Filtro de Outlier Apex: Velocidades irreais
        if 'Speed' in telemetry_cleaned.columns:
            telemetry_cleaned = telemetry_cleaned[telemetry_cleaned['Speed'] <= 375]

        # Salva em Parquet (Alta Performance)
        telemetry_cleaned.to_parquet(f'{pasta_limpa}/{ano}_{local}_telemetry_cleaned.parquet')
        
        print(f"✅ Sucesso: {local} finalizado e salvo em /{pasta_limpa}")

    except Exception as e:
        print(f"❌ Erro em {local}: {e}")

# Execução do Pipeline
for ano, local in corridas:
    extrair_e_limpar_sessao(ano, local)

print("\n--- PIPELINE CONCLUÍDO: Dados prontos para o Tableau ---")