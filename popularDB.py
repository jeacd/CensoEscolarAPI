import pandas as pd
import psycopg2
import requests
import time
import json
from pathlib import Path


arquivos_csv = ['microdados_ed_basica_2023.csv','microdados_ed_basica_2024.csv']
colunas_desejadas = [
    'NO_REGIAO', 'CO_REGIAO', 'CO_UF', 'CO_MUNICIPIO', 'CO_MESORREGIAO',
    'CO_MICRORREGIAO', 'NO_ENTIDADE', 'CO_ENTIDADE',
    'QT_MAT_BAS', 'QT_MAT_INF', 'QT_MAT_FUND', 'QT_MAT_MED',
    'QT_MAT_EJA', 'QT_MAT_ESP'
]
chunk_size = 1000
cache_file = Path("cache_ibge.json")


if cache_file.exists():
    with cache_file.open("r", encoding="utf-8") as f:
        cache = json.load(f)
else:
    cache = {}

def salvar_cache():
    with cache_file.open("w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False)

# obter os dados corretos de micro e meso região
def obter_codigos_ibge(co_municipio: str):
    if co_municipio in cache:
        return cache[co_municipio]

    url = f"https://servicodados.ibge.gov.br/api/v1/localidades/municipios/{co_municipio}"

    for tentativa in range(5):
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            dados = resp.json()

            co_micro = dados["microrregiao"]["id"]
            co_meso  = dados["microrregiao"]["mesorregiao"]["id"]

            cache[co_municipio] = (co_meso, co_micro)
            time.sleep(0.15)
            return co_meso, co_micro

        except Exception as e:
            print(f"Erro ao obter {co_municipio}: {e} - tentativa {tentativa+1}/5")
            time.sleep(2 ** tentativa)

    raise RuntimeError(f"Falha ao obter dados para {co_municipio} após 5 tentativas")

conn = psycopg2.connect(
    dbname='censoescolar',
    user='postgres',
    password='123456789',
    host='localhost',
    port='5434'
)
cursor = conn.cursor()

def inserir_parcelar_dados(df):
    for _, row in df.iterrows():
        co_municipio = str(row.get('CO_MUNICIPIO'))

        # Os dados microrregião e mesorregião estão incorretos, então é preciso corrigir
        try:
            co_meso, co_micro = obter_codigos_ibge(co_municipio)
        except Exception as e:
            print(f"Erro na correção para município {co_municipio}: {e}")
            co_meso = row.get('CO_MESORREGIAO')
            co_micro = row.get('CO_MICRORREGIAO')

        def safe_int(val):
            return int(val) if pd.notna(val) else 0

        cursor.execute("""
            INSERT INTO tb_instituicao (
                ano, no_regiao, co_regiao, co_uf, co_municipio, co_mesorregiao,
                co_microrregiao, no_entidade, co_entidade,
                qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med,
                qt_mat_eja, qt_mat_esp
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row.get('NU_ANO'),
            row.get('NO_REGIAO'),
            row.get('CO_REGIAO'),
            row.get('CO_UF'),
            co_municipio,
            co_meso,
            co_micro,
            row.get('NO_ENTIDADE'),
            row.get('CO_ENTIDADE'),
            safe_int(row.get('QT_MAT_BAS')),
            safe_int(row.get('QT_MAT_INF')),
            safe_int(row.get('QT_MAT_FUND')),
            safe_int(row.get('QT_MAT_MED')),
            safe_int(row.get('QT_MAT_EJA')),
            safe_int(row.get('QT_MAT_ESP'))
        ))


for arquivo in arquivos_csv:
    print(f"Processando: {arquivo}")
    for chunk in pd.read_csv(arquivo, sep=';', encoding='latin1', chunksize=chunk_size):
        colunas_existentes = [col for col in colunas_desejadas if col in chunk.columns]
        chunk_filtrado = chunk[colunas_existentes]
        inserir_parcelar_dados(chunk_filtrado)
        conn.commit()
        salvar_cache()
        print(f"Chunk de {len(chunk_filtrado)} linhas inserido.")

cursor.close()
conn.close()