# import requests

# url = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados'
# db = 'http://127.0.0.1:5000/uf'

# response = requests.get(url)
# ufs_filtrar = {24, 25, 26}
# dados = response.json()

# for estado in dados:
#     if estado['id'] in ufs_filtrar:
#         response = requests.post(db, json=estado)


import requests
import psycopg2

url = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados'

response = requests.get(url)
dados = response.json()

conn = psycopg2.connect(
    dbname='censoescolar',
    user='postgres',
    password='123456789',
    host='localhost',
    port='5434'
)
cursor = conn.cursor()

for estado in dados:
    cursor.execute("""
        INSERT INTO tb_uf (id, sigla, nome)
        VALUES (%s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """, (estado['id'], estado['sigla'], estado['nome']))

conn.commit()
cursor.close()
conn.close()