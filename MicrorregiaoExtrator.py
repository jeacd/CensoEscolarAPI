# import requests
        
# url = 'https://servicodados.ibge.gov.br/api/v1/localidades/microrregioes'
# db = 'http://127.0.0.1:5000/microrregiao'

# response = requests.get(url)
# ufs_filtrar = {24, 25, 26}
# dados = response.json()
# for microrregiao in dados:
#     if microrregiao['mesorregiao']['UF']['id'] in ufs_filtrar:
#         requests.post(db, json=microrregiao)


import requests
import psycopg2

url = 'https://servicodados.ibge.gov.br/api/v1/localidades/microrregioes'

response = requests.get(url)
microrregioes = response.json()

conn = psycopg2.connect(
    dbname='censoescolar',
    user='postgres',
    password='123456789',
    host='localhost',
    port='5434'
)
cursor = conn.cursor()

for microrregiao in microrregioes:
    cursor.execute("""
        INSERT INTO tb_microrregiao (id, nome, co_uf)
        VALUES (%s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """, (microrregiao['id'], microrregiao['nome'], microrregiao['mesorregiao']['UF']['id']))

conn.commit()
cursor.close()
conn.close()