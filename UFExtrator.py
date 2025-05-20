import requests

url = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados'
db = 'http://127.0.0.1:5000/uf'

response = requests.get(url)
ufs_filtrar = {24, 25, 26}
dados = response.json()

for estado in dados:
    if estado['id'] in ufs_filtrar:
        response = requests.post(db, json=estado)