from flask import Flask, jsonify, request
import sqlite3

from models.instituicaoEnsino import InstituicaoEnsino

app = Flask(__name__)

def validarInstituicao(content):
    if content.get('CO_UF') is None:
        return False
    elif int(content['CO_UF']) < 11 or int(content['CO_UF']) > 55:
        return False
    else:
        return True


def funcoesDb(metodo, data=None):
    try:
        conn = sqlite3.connect('censoescolar.db')
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
            
            for row in resultSet:
                id = row[0]
                NO_REGIAO = row[2]
                CO_REGIAO = row[3]
                NO_UF = row[4]
                CO_UF = row[5]
                NO_MUNICIPIO = row[6]
                CO_MUNICIPIO = row[7]
                NO_MESORREGIAO = row[8]
                CO_MESORREGIAO = row[9]
                NO_MICRORREGIAO = row[10]
                CO_MICRORREGIAO = row[11]
                NO_ENTIDADE = row[12]
                CO_ENTIDADE = row[13]
                QT_MAT_BAS = row[14]
                QT_MAT_INF = row[15]
                QT_MAT_FUND = row[16]
                QT_MAT_MED = row[17]
                QT_MAT_EJA = row[18]
                QT_MAT_ESP = row[19]

                instituicaoEnsino = InstituicaoEnsino(id,
                    NO_REGIAO=NO_REGIAO,
                    CO_REGIAO=CO_REGIAO,
                    NO_UF=NO_UF,
                    CO_UF=CO_UF,
                    NO_MUNICIPIO=NO_MUNICIPIO,
                    CO_MUNICIPIO=CO_MUNICIPIO,
                    NO_MESORREGIAO=NO_MESORREGIAO,
                    CO_MESORREGIAO=CO_MESORREGIAO,
                    NO_MICRORREGIAO=NO_MICRORREGIAO,
                    CO_MICRORREGIAO=CO_MICRORREGIAO,
                    NO_ENTIDADE=NO_ENTIDADE,
                    CO_ENTIDADE=CO_ENTIDADE,
                    QT_MAT_BAS=QT_MAT_BAS,
                    QT_MAT_INF=QT_MAT_INF,
                    QT_MAT_FUND=QT_MAT_FUND,
                    QT_MAT_MED=QT_MAT_MED,
                    QT_MAT_EJA=QT_MAT_EJA,
                    QT_MAT_ESP=QT_MAT_ESP
                )

                instituicoesEnsino.append(instituicaoEnsino.toDict())
                
            return instituicoesEnsino
        elif (metodo == 'GETONE'):
            try:
                cur.execute('''
                    SELECT * FROM tb_instituicao WHERE CO_ENTIDADE = ?
                ''', (int(data),))
                resultSet = cur.fetchone()
                
                id = resultSet[0]
                NO_REGIAO = resultSet[2]
                CO_REGIAO = resultSet[3]
                NO_UF = resultSet[4]
                CO_UF = resultSet[5]
                NO_MUNICIPIO = resultSet[6]
                CO_MUNICIPIO = resultSet[7]
                NO_MESORREGIAO = resultSet[8]
                CO_MESORREGIAO = resultSet[9]
                NO_MICRORREGIAO = resultSet[10]
                CO_MICRORREGIAO = resultSet[11]
                NO_ENTIDADE = resultSet[12]
                CO_ENTIDADE = resultSet[13]
                QT_MAT_BAS = resultSet[14]
                QT_MAT_INF = resultSet[15]
                QT_MAT_FUND = resultSet[16]
                QT_MAT_MED = resultSet[17]
                QT_MAT_EJA = resultSet[18]
                QT_MAT_ESP = resultSet[19]
                
                instituicaoEnsino = InstituicaoEnsino(id,
                        NO_REGIAO=NO_REGIAO,
                        CO_REGIAO=CO_REGIAO,
                        NO_UF=NO_UF,
                        CO_UF=CO_UF,
                        NO_MUNICIPIO=NO_MUNICIPIO,
                        CO_MUNICIPIO=CO_MUNICIPIO,
                        NO_MESORREGIAO=NO_MESORREGIAO,
                        CO_MESORREGIAO=CO_MESORREGIAO,
                        NO_MICRORREGIAO=NO_MICRORREGIAO,
                        CO_MICRORREGIAO=CO_MICRORREGIAO,
                        NO_ENTIDADE=NO_ENTIDADE,
                        CO_ENTIDADE=CO_ENTIDADE,
                        QT_MAT_BAS=QT_MAT_BAS,
                        QT_MAT_INF=QT_MAT_INF,
                        QT_MAT_FUND=QT_MAT_FUND,
                        QT_MAT_MED=QT_MAT_MED,
                        QT_MAT_EJA=QT_MAT_EJA,
                        QT_MAT_ESP=QT_MAT_ESP
                    )
                
                return instituicaoEnsino.toDict()
            except:
                return jsonify({'mensagem': 'Instituição não encontrada'}), 404
        elif (metodo == 'POST'):
            cur.execute('''
                    INSERT INTO tb_instituicao (
                        NO_REGIAO, CO_REGIAO, NO_UF, CO_UF,
                        NO_MUNICIPIO, CO_MUNICIPIO,
                        NO_MESORREGIAO, CO_MESORREGIAO,
                        NO_MICRORREGIAO, CO_MICRORREGIAO,
                        NO_ENTIDADE, CO_ENTIDADE,
                        QT_MAT_BAS, QT_MAT_INF, QT_MAT_FUND,
                        QT_MAT_MED, QT_MAT_EJA, QT_MAT_ESP
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''',
                        (
                            data["NO_REGIAO"], data["CO_REGIAO"], data["NO_UF"], data["CO_UF"],
                            data["NO_MUNICIPIO"], data["CO_MUNICIPIO"],
                            data["NO_MESORREGIAO"], data["CO_MESORREGIAO"],
                            data["NO_MICRORREGIAO"], data["CO_MICRORREGIAO"],
                            data["NO_ENTIDADE"], data["CO_ENTIDADE"],
                            data["QT_MAT_BAS"], data["QT_MAT_INF"], data["QT_MAT_FUND"],
                            data["QT_MAT_MED"], data["QT_MAT_EJA"], data["QT_MAT_ESP"]
                        )
            )
            conn.commit()

            id = cur.lastrowid
            institucao = InstituicaoEnsino(id, data["NO_REGIAO"], data["CO_REGIAO"], data["NO_UF"], data["CO_UF"],
                                        data["NO_MUNICIPIO"], data["CO_MUNICIPIO"],
                                        data["NO_MESORREGIAO"], data["CO_MESORREGIAO"],
                                        data["NO_MICRORREGIAO"], data["CO_MICRORREGIAO"],
                                        data["NO_ENTIDADE"], data["CO_ENTIDADE"],
                                        data["QT_MAT_BAS"], data["QT_MAT_INF"], data["QT_MAT_FUND"],
                                        data["QT_MAT_MED"], data["QT_MAT_EJA"], data["QT_MAT_ESP"])

            
            return institucao.toDict()
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
    except:
        jsonify({'mensagem': 'Problema com o banco de dados'}), 500
    finally:
        conn.close()


@app.get('/instituicoesensino')
def getInstituicoesEnsino():
    pagina = int(request.args.get('pagina', 1))
    tamanho = int(request.args.get('tamanho', 10))
    conteudoRequisicao = {'pagina': pagina, 'tamanho': tamanho}

    resultadoRequisicao = funcoesDb('GETALL', conteudoRequisicao)
    return jsonify(resultadoRequisicao), 200


@app.get('/instituicoesensino/<cod_entidade>')
def getInstituicaoEnsino(cod_entidade):
    resultadoRequisicao = funcoesDb('GETONE', cod_entidade)
    return resultadoRequisicao


@app.delete('/instituicoesensino/<cod_entidade>')
def deleteInstituicaoEnsino(cod_entidade):
    resultadoRequisicao = funcoesDb('DELETE', cod_entidade)
    return resultadoRequisicao


@app.post('/instituicoesensino')
def postInstituicaoEnsino():
    conteudoRequisicao = request.get_json()
    isValid = validarInstituicao(conteudoRequisicao)

    if (isValid):
        resultadoRequisicao = funcoesDb('POST', conteudoRequisicao)
        return jsonify(resultadoRequisicao), 200
    else:
        return jsonify({'erro': 'Instituição não cadastrada'}), 406


@app.put('/instituicoesensino')
def updateInstituicaoEnsino():
    conteudoRequisicao = request.get_json()
    resultadoRequisicao = funcoesDb('UPDATE', conteudoRequisicao)
    return resultadoRequisicao


if __name__ == '__main__':
    app.run()

# dbreaver
