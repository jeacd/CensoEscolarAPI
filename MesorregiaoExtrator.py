import requests
        
url = 'https://servicodados.ibge.gov.br/api/v1/localidades/mesorregioes'
db = 'http://127.0.0.1:5000/mesorregiao'

response = requests.get(url)
ufs_filtrar = {24, 25, 26}
dados = response.json()
for mesorregiao in dados:
    if mesorregiao['UF']['id'] in ufs_filtrar:
        requests.post(db, json=mesorregiao)