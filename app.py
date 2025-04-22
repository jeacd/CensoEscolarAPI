from flask import Flask, jsonify
import json

app = Flask(__name__)

def lerJson():
    with open('dados.json', mode='r', encoding='utf-8') as json_file:
        dados = json.load(json_file)
        return dados

def escreverJson(dados):
    with open('dados.json', mode='w', encoding='utf-8') as json_file:
        json.dump(dados, json_file, ensure_ascii=False, indent=4)


@app.get('/instituicoesensino')
def getInstituicoesEnsino():
    instituicoes = lerJson()
    return jsonify(instituicoes), 200

@app.get('/instituicoesensino/<cod_entidade>')
def getInstituicaoEnsino(cod_entidade):
    instituicoes = lerJson()
    instituicoesFiltradas = [instituicao for instituicao in instituicoes if instituicao['CO_ENTIDADE'] == cod_entidade]
    
    if len(instituicoesFiltradas) > 0:
        return jsonify(instituicoesFiltradas), 200
    else:
        return jsonify({'Erro': 'ID não encontrado'}), 404
    
@app.delete('/instituicoesensino/<cod_entidade>')
def deleteInstituicaoEnsino(cod_entidade):
    instituicoes = lerJson()
    instituicoesAposDelete = [instituicao for instituicao in instituicoes if instituicao['CO_ENTIDADE'] != cod_entidade]
    
    if len(instituicoesAposDelete) < len(instituicoes):
        escreverJson(instituicoesAposDelete)
        return jsonify({'mensagem': 'Delete realizado com sucesso'}), 200
    else:
        return jsonify({'Erro': 'Instituição não encontrada'}), 404


if __name__ == '__main__':
    app.run()
