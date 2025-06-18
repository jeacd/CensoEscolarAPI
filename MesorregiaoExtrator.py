# import requests
        
# url = 'https://servicodados.ibge.gov.br/api/v1/localidades/mesorregioes'
# db = 'http://127.0.0.1:5000/mesorregiao'

# response = requests.get(url)
# ufs_filtrar = {24, 25, 26}
# dados = response.json()
# for mesorregiao in dados:
#     if mesorregiao['UF']['id'] in ufs_filtrar:
#         requests.post(db, json=mesorregiao)
        
import requests
import psycopg2

url = 'https://servicodados.ibge.gov.br/api/v1/localidades/mesorregioes'

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

for mesorregiao in dados:
    cursor.execute("""
        INSERT INTO tb_mesorregiao (id, nome, co_uf)
        VALUES (%s, %s, %s)
        ON CONFLICT (id) DO NOTHING
    """, (mesorregiao['id'], mesorregiao['nome'], mesorregiao['UF']['id']))

conn.commit()
cursor.close()
conn.close()