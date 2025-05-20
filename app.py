from flask import Flask, jsonify, request, g
from marshmallow import ValidationError
import sqlite3

from models.instituicaoEnsino import InstituicaoEnsino
from models.instituicaoEnsino import InstituicaoEnsinoSchema
from models.uf import Uf
from models.mesorregiao import Mesorregiao
from models.microrregiao import Microrregiao
from models.municipio import Municipio

app = Flask(__name__)

DATABASE = 'censoescolar.db'

def make_dicts(cursor, row):
    return {cursor.description[idx][0]: value for idx, value in enumerate(row)}

def getConnection():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    db.row_factory = make_dicts
    return db

@app.teardown_appcontext
def closeConnection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def funcoesDb(metodo, data=None):
    try:
        conn = getConnection()
        cur = conn.cursor()
        
        if (metodo == 'GETALL'):
            instituicoesEnsino = []
            
            pagina = data['pagina']
            tamanho = data['tamanho']
            offset = (pagina - 1) * tamanho

            cur.execute('''
                SELECT * FROM tb_instituicao
                LIMIT ? OFFSET ?
            ''', (tamanho, offset))
            resultSet = cur.fetchall()
            
            for instituicao in resultSet:
                instituicaoEnsino = InstituicaoEnsino(**instituicao)
                instituicoesEnsino.append(instituicaoEnsino)
                
            return instituicoesEnsino
        elif (metodo == 'GETONE'):
            try:
                cur.execute('''
                    SELECT * FROM tb_instituicao WHERE CO_ENTIDADE = ?
                ''', (int(data),))
                resultSet = cur.fetchone()
                
                instituicaoEnsino = InstituicaoEnsino(**resultSet)
                
                return instituicaoEnsino
            except Exception as e:
                print("Erro:", e)
                return jsonify({'mensagem': 'Erro ao buscar instituição'}), 500
        elif (metodo == 'POST'):
            cur.execute('''
                    INSERT INTO tb_instituicao (
                        NO_REGIAO, CO_REGIAO, CO_UF,
                        CO_MUNICIPIO,
                        CO_MESORREGIAO,
                        CO_MICRORREGIAO,
                        NO_ENTIDADE, CO_ENTIDADE,
                        QT_MAT_BAS, QT_MAT_INF, QT_MAT_FUND,
                        QT_MAT_MED, QT_MAT_EJA, QT_MAT_ESP
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''',
                        (
                            data["NO_REGIAO"], data["CO_REGIAO"], data["CO_UF"],
                            data["CO_MUNICIPIO"],
                            data["CO_MESORREGIAO"],
                            data["CO_MICRORREGIAO"],
                            data["NO_ENTIDADE"], data["CO_ENTIDADE"],
                            data["QT_MAT_BAS"], data["QT_MAT_INF"], data["QT_MAT_FUND"],
                            data["QT_MAT_MED"], data["QT_MAT_EJA"], data["QT_MAT_ESP"]
                        )
            )
            conn.commit()
            
            data['id'] = cur.lastrowid
            institucao = InstituicaoEnsino(**data)

            
            return institucao
        elif (metodo == 'DELETE'):
            try:
                cur.execute('''
                DELETE FROM tb_instituicao WHERE CO_ENTIDADE = ?
                ''', (data,))
                conn.commit()
                return jsonify({'mensagem': 'Instituição removida'}), 200
            except:
                return jsonify({'mensagem': 'Instituição não removida'}), 404
        elif (metodo == 'UPDATE'):
            try:
                cur.execute('''
                    UPDATE tb_instituicao SET NO_ENTIDADE = ? WHERE CO_ENTIDADE = ?;
                    ''', (data['NO_ENTIDADE'], int(data['CO_ENTIDADE']))
                )
                conn.commit()
                return jsonify({'mensagem': 'Instituição atualizada com sucesso!'}), 200
            except:
                return jsonify({'mensagem': 'Instituição não encontrada.'}), 404
    except sqlite3.Error as e:
        return jsonify({'mensagem': 'Problema com o banco de dados: {e}'}), 500


@app.get('/instituicoesensino')
def getInstituicoesEnsino():
    pagina = int(request.args.get('pagina', 1))
    tamanho = int(request.args.get('tamanho', 5))
    conteudoRequisicao = {'pagina': pagina, 'tamanho': tamanho}

    resultadoRequisicao = funcoesDb('GETALL', conteudoRequisicao)
    
    schema = InstituicaoEnsinoSchema(many=True)
    return jsonify(schema.dump(resultadoRequisicao)), 200


@app.get('/instituicoesensino/<cod_entidade>')
def getInstituicaoEnsino(cod_entidade):
    resultadoRequisicao = funcoesDb('GETONE', cod_entidade)
    schema = InstituicaoEnsinoSchema()
    return jsonify(schema.dump(resultadoRequisicao)), 200


@app.delete('/instituicoesensino/<cod_entidade>')
def deleteInstituicaoEnsino(cod_entidade):
    resultadoRequisicao = funcoesDb('DELETE', cod_entidade)
    return resultadoRequisicao


@app.post('/instituicoesensino')
def postInstituicaoEnsino():
    schema = InstituicaoEnsinoSchema()
    try:
        conteudoRequisicao = schema.load(request.get_json())
        print(conteudoRequisicao)
    except ValidationError as err:
        return jsonify({'mensagem': err.messages}), 400

    resultadoRequisicao = funcoesDb('POST', conteudoRequisicao)
    return jsonify(schema.dump(resultadoRequisicao)), 201


@app.put('/instituicoesensino')
def updateInstituicaoEnsino():
    schema = InstituicaoEnsinoSchema()
    try:
        conteudoRequisicao = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'mensagem': err.messages}), 400

    resultadoRequisicao = funcoesDb('UPDATE', conteudoRequisicao)
    return resultadoRequisicao, 200




'---------------------------REQUISIÇÕES PARA UF------------------------------'
@app.post('/uf')
def postUf():
    conteudoRequisicao = request.get_json()
    
    conn = getConnection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO tb_uf (
            id, sigla, nome
        ) VALUES (?, ?, ?)
        ''',
        (
            conteudoRequisicao["id"], conteudoRequisicao["sigla"], conteudoRequisicao["nome"]
        )
    )
    conn.commit()
    conn.close()
    
    uf = Uf(**conteudoRequisicao)
    
    return jsonify(uf.toDict()), 200

'---------------------------REQUISIÇÕES PARA MESORREGIAO------------------------------'
@app.post('/mesorregiao')
def postMesorregiao():
    conteudoRequisicao = request.get_json()
    
    conn = getConnection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO tb_mesorregiao (
            id, nome, co_uf
        ) VALUES (?, ?, ?)
        ''',
        (
            conteudoRequisicao["id"], conteudoRequisicao["nome"], conteudoRequisicao["UF"]['id']
        )
    )
    conn.commit()
    conn.close()
    
    mesorregiao = Mesorregiao(**conteudoRequisicao)
    
    return jsonify(mesorregiao.toDict()), 200

'---------------------------REQUISIÇÕES PARA MICRORREGIAO------------------------------'
@app.post('/microrregiao')
def postMicrorregiao():
    conteudoRequisicao = request.get_json()
    
    conn = getConnection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO tb_microrregiao (
            id, nome, co_uf
        ) VALUES (?, ?, ?)
        ''',
        (
            conteudoRequisicao["id"], conteudoRequisicao["nome"], conteudoRequisicao['mesorregiao']['UF']['id']
        )
    )
    conn.commit()
    conn.close()
    
    microrregiao = Microrregiao(**conteudoRequisicao)
    
    return jsonify(microrregiao.toDict()), 200

'---------------------------REQUISIÇÕES PARA MUNICIPIO------------------------------'
@app.post('/municipio')
def postMunicipio():
    conteudoRequisicao = request.get_json()
    
    conn = getConnection()
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO tb_municipio (
            id, nome, co_uf, co_mesorrwegiao, co_microrregiao
        ) VALUES (?, ?, ?, ?, ?)
        ''',
        (
            conteudoRequisicao["id"], conteudoRequisicao["nome"], conteudoRequisicao['co_uf'],
            conteudoRequisicao['co_mesorregiao'], conteudoRequisicao['co_microrregiao']
        )
    )
    conn.commit()
    conn.close()
    
    municipio = Municipio(**conteudoRequisicao)
    
    return jsonify(municipio.toDict()), 200

if __name__ == '__main__':
    app.run()

