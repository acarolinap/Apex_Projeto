import fastf1
import pandas as pd
import os

# Configura o cache para o script não baixar a mesma coisa duas vezes da internet (acelera MUITO o processo)
if not os.path.exists('cache_f1'):
    os.makedirs('cache_f1')
fastf1.Cache.enable_cache('cache_f1')

# Dicionário com as corridas do escopo e os IDs da Base Apex
corridas = {
    'Saudi Arabia': 1122,
    'Monaco': 1128,
    'Silverstone': 1132,
    'Hungary': 1133
}

pilotos = ['NOR', 'PIA']
todas_telemetrias = []

print("Iniciando extração em lote da Telemetria...")

# O loop vai passar por cada país automaticamente
for nome_pista, race_id in corridas.items():
    print(f"\n-> Baixando dados de {nome_pista}...")
    try:
        # Carrega a sessão da corrida (R = Race)
        session = fastf1.get_session(2024, nome_pista, 'R')
        session.load(telemetry=True, weather=False, messages=False)

        for piloto in pilotos:
            print(f"   Extraindo telemetria de {piloto}...")
            # Pega a volta mais rápida do piloto específico
            lap = session.laps.pick_driver(piloto).pick_fastest()
            
            # Puxa a telemetria de velocidade/distância
            tel = lap.get_telemetry()
            
            # CRÍTICO: Cria as colunas que estavam faltando pro Tableau!
            tel['Driver'] = piloto
            tel['raceId'] = race_id
            tel['RaceName'] = nome_pista
            tel['LapNumber'] = 1 # Definimos como 1 para facilitar os filtros no Tableau
            
            todas_telemetrias.append(tel)
            
    except Exception as e:
        print(f"Erro ao processar {nome_pista} - {piloto}: {e}")

# Junta tudo em um único arquivo
if todas_telemetrias:
    print("\nConsolidando todos os dados em uma tabela mestre...")
    telemetria_completa = pd.concat(todas_telemetrias, ignore_index=True)
    
    # Filtra só as colunas que importam para não explodir a memória do Tableau
    colunas_pro_tableau = ['Distance', 'Speed', 'Time', 'Driver', 'raceId', 'RaceName', 'LapNumber']
    telemetria_final = telemetria_completa[colunas_pro_tableau]
    
    # Salva o arquivo CSV definitivo
    telemetria_final.to_csv('Telemetria_Mestra_Apex_REAL.csv', index=False)
    print("\nSucesso! O arquivo 'Telemetria_Mestra_Apex_REAL.csv' foi gerado.")
else:
    print("\nNenhum dado foi extraído. Verifique sua conexão.")