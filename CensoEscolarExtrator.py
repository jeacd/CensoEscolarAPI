import json
import requests

arquivo = 'dados.json'

url = 'http://127.0.0.1:5000/instituicoesensino'

with open(arquivo, 'r', encoding='utf-8') as f:
    dados = json.load(f)

for item in dados:
    requests.post(url, json=item)
