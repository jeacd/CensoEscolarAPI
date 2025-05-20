import requests
        
url = 'https://servicodados.ibge.gov.br/api/v1/localidades/microrregioes'
db = 'http://127.0.0.1:5000/microrregiao'

response = requests.get(url)
ufs_filtrar = {24, 25, 26}
dados = response.json()
for microrregiao in dados:
    if microrregiao['mesorregiao']['UF']['id'] in ufs_filtrar:
        requests.post(db, json=microrregiao)