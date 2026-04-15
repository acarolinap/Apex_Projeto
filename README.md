# Apex Analytics: F1 Performance & Strategy BI

![F1 Data Analysis](https://img.shields.io/badge/Status-In%20Development-orange)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Tableau](https://img.shields.io/badge/Visualização-Tableau-blue?logo=tableau)
![FastF1](https://img.shields.io/badge/Data%20Source-FastF1-red)

## Sobre o Projeto
O **Apex Analytics** é um projeto de Business Intelligence e Ciência de Dados focado na análise de performance da Fórmula 1 moderna. O objetivo central é transformar telemetria bruta e dados históricos em modelos preditivos e descritivos para otimização de estratégia em pista e análise de risco competitivo.

## Perguntas de Pesquisa (Escopo do Projeto)
Nossa análise é guiada por cinco eixos fundamentais que cruzam estratégia, telemetria e gestão de risco:

1. **Análise de Risco na Estratégia (Degradação vs. Pit Stop):** Qual é o ponto de inflexão exato (limite de risco) na degradação dos pneus em que a perda de tempo acumulada na pista supera o tempo total gasto para fazer um pit stop extra?
2. **Comparativo de Estilo de Pilotagem (Telemetria Isolada):** Ao analisar a telemetria de dois companheiros da mesma equipe, em quais trechos específicos do circuito (frenagem tardia vs. reaceleração antecipada) o piloto mais rápido constrói sua vantagem?
3. **Impacto de Variáveis Externas (Clima e Desgaste):** Existe uma correlação matematicamente observável entre a temperatura do asfalto (TrackTemp) e a piora progressiva no tempo de volta ao longo de 15 voltas com pneus macios?
4. **Eficiência de Processos Críticos (Largada):** Nos circuitos da temporada de 2026, qual é a probabilidade estatística de o pole position perder a liderança antes da primeira zona de frenagem forte, e como o tempo de reação de 0 a 100 km/h afeta esse risco?
5. **Gestão de Risco em Ultrapassagens (Zonas de DRS):** Qual é a taxa real de conversão de ultrapassagens quando o delta de perseguição é inferior a 0.5s comparado ao limite de ativação de 0.8s a 1.0s?

## Arquitetura de Dados & ETL
Implementamos um pipeline de **ETL (Extract, Transform, Load)** em Python para garantir que os dados consumidos no Tableau estejam normalizados.

### O Recorte Estratégico (2018 - 2026)
Utilizamos exclusivamente dados de **2018 em diante**. 
* **Justificativa:** A padronização da telemetria de alta resolução ($10~Hz$) pela FIA a partir de 2018 permite a análise precisa de telemetria exigida pelas perguntas 2, 4 e 5, eliminando discrepâncias de sistemas de cronometragem obsoletos.

### Saneamento e Limpeza
* **Normalização:** Substituição de ruídos de banco de dados (`\N`) por valores nulos reais.
* **Filtros de Sinal:** Limpeza de telemetria binária para remover picos de sensores irreais (velocidades > 375 km/h).
* **Parquet vs CSV:** Armazenamento colunar (Parquet) para dados de sensores pesados e CSV para metadados, otimizando o carregamento do Dashboard.

## Estrutura do Repositório
```text
├── data/
│   ├── raw/                # Dados brutos de sessão e clima
│   └── cleaned/            # Dados processados prontos para análise
├── scripts/
│   └── limpeza_apex.py     # Script mestre de ETL (Python)
├── notebooks/              # Análises exploratórias
└── README.md

Equipe Apex Analytics

Carolina (Líder do Projeto e Engenheira de Dados)
Juan (Ingestão e Coleta de Telemetria)
Diego (Visualização e BI - Tableau)
Kaue (Regras de Negócio e Análise de Status)
Lucas (Tipagem e Integridade de Dados)

Este projeto foi desenvolvido para fins acadêmicos na UNISUL (2026).