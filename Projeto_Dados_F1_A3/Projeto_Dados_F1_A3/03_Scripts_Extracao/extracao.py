import fastf1
import pandas as pd
import os


fastf1.Cache.enable_cache('cache_fastf1')
os.makedirs('dados_brutos_f1', exist_ok=True)


corridas = [
    (2024, 'Hungary'),     # Calor extremo (Pergunta 3)
    (2024, 'Silverstone'),  # Clima instável (Pergunta 3)
    (2024, 'Saudi Arabia'), # Alta velocidade/Telemetria (Pergunta 2)
    (2024, 'Monaco')        # Baixa velocidade/Aceleração (Pergunta 2)
]
def extrair_pacote_completo(ano, local):
    print(f"\n--- Extraindo: {local} {ano} ---")
    session = fastf1.get_session(ano, local, 'R')
    session.load()

  
    laps = session.laps
    laps.to_csv(f'dados_brutos_f1/{ano}_{local}_laps.csv', index=False)

    weather = session.weather_data
    weather.to_csv(f'dados_brutos_f1/{ano}_{local}_weather.csv', index=False)

    fastest = laps.pick_fastest()
    telemetry = fastest.get_telemetry()
    telemetry.to_parquet(f'dados_brutos_f1/{ano}_{local}_telemetry.parquet')
    
    print(f"Finalizado: {local}")

for ano, local in corridas:
    extrair_pacote_completo(ano, local)

print("\n--- INGESTÃO CONCLUÍDA: Todos os arquivos estão na pasta 'dados_brutos_f1' ---")