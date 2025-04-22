from flask import Flask, jsonify, request
import json

app = Flask(__name__)

def lerJson():
    with open('dados.json', mode='r', encoding='utf-8') as json_file:
        dados = json.load(json_file)
        return dados

def escreverJson(dados):
    with open('dados.json', mode='w', encoding='utf-8') as json_file:
        json.dump(dados, json_file, ensure_ascii=False, indent=4)

def validarInstituicao(content):
    if content.get('CO_UF') is None:
        return False
    elif int(content['CO_UF']) < 11 or int(content['CO_UF']) > 55:
        return False
    else:
        return True

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
        return jsonify({'erro': 'Instituição não encontrada'}), 404
    
@app.delete('/instituicoesensino/<cod_entidade>')
def deleteInstituicaoEnsino(cod_entidade):
    instituicoes = lerJson()
    instituicoesFiltradas = [instituicao for instituicao in instituicoes if instituicao['CO_ENTIDADE'] != cod_entidade]
    
    if len(instituicoesFiltradas) < len(instituicoes):
        escreverJson(instituicoesFiltradas)
        return jsonify({'mensagem': 'Instituição removida com sucesso'}), 200
    else:
        return jsonify({'erro': 'Instituição não encontrada'}), 404

@app.post('/instituicoesensino')
def postInstituicaoEnsino():
    instituicoes = lerJson()
    content = request.get_json()
    isValid = validarInstituicao(content)
    
    if (isValid):
        instituicoes.append(content)
        escreverJson(instituicoes)
        return jsonify({"mensagem": "Cadastro realizado", "dados": content}), 200
    
    return jsonify({'erro': 'Instituição não cadastrada'}), 406

@app.put('/instituicoesensino')
def updateInstituicaoEnsino():
    instituicoes = lerJson()
    content = request.get_json()
    countIndex = -1
    instituicaoEncontrada = False
    
    for instituicao in instituicoes:
        countIndex = countIndex + 1
        if instituicao['CO_ENTIDADE'] == content['CO_ENTIDADE']:
            instituicaoEncontrada = True
            break
        
    if instituicaoEncontrada:
        instituicoes[countIndex].update(content)
        escreverJson(instituicoes)
        return jsonify({'message': 'Instituição atualizada com sucesso!'}), 200
    else:
        return jsonify({'erro': 'Instituição não encontrada.'}), 404
            

if __name__ == '__main__':
    app.run()
