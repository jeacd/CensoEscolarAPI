# import requests

# url = 'https://servicodados.ibge.gov.br/api/v1/localidades/municipios'
# db = 'http://127.0.0.1:5000/municipio'

# response = requests.get(url)
# ufs_filtrar = {24, 25, 26}
# dados = response.json()
# for municipio in dados:
#     microrregiao = municipio.get('microrregiao')
#     mesorregiao = microrregiao.get('mesorregiao') if microrregiao else None
#     uf = mesorregiao.get('UF') if mesorregiao else None

#     if uf and uf.get('id') in ufs_filtrar:
#         data = {
#             'id': municipio['id'],
#             'nome': municipio['nome'],
#             'co_uf': uf['id'],
#             'co_mesorregiao': mesorregiao['id'],
#             'co_microrregiao': microrregiao['id']
#         }
#         requests.post(db, json=data)

import requests
import psycopg2

url = 'https://servicodados.ibge.gov.br/api/v1/localidades/municipios'
response = requests.get(url)
municipios = response.json()

conn = psycopg2.connect(
    dbname='censoescolar',
    user='postgres',
    password='123456789',
    host='localhost',
    port='5434'
)
cursor = conn.cursor()

for municipio in municipios:
    microrregiao = municipio['microrregiao']
    mesorregiao = False
    uf = ''
    if microrregiao:
        mesorregiao = microrregiao['mesorregiao']
        uf = mesorregiao['UF']
    
    if mesorregiao:
        cursor.execute("""
        INSERT INTO tb_municipio (id, nome, co_uf, co_mesorregiao, co_microrregiao)
        VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (id) DO NOTHING
        """, (
            municipio['id'],
            municipio['nome'],
            uf['id'],
            mesorregiao['id'],
            microrregiao['id']
        ))

conn.commit()
cursor.close()
conn.close()