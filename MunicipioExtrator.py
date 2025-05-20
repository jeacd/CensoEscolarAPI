import requests

url = 'https://servicodados.ibge.gov.br/api/v1/localidades/municipios'
db = 'http://127.0.0.1:5000/municipio'

response = requests.get(url)
ufs_filtrar = {24, 25, 26}
dados = response.json()
for municipio in dados:
    microrregiao = municipio.get('microrregiao')
    mesorregiao = microrregiao.get('mesorregiao') if microrregiao else None
    uf = mesorregiao.get('UF') if mesorregiao else None

    if uf and uf.get('id') in ufs_filtrar:
        data = {
            'id': municipio['id'],
            'nome': municipio['nome'],
            'co_uf': uf['id'],
            'co_mesorregiao': mesorregiao['id'],
            'co_microrregiao': microrregiao['id']
        }
        requests.post(db, json=data)