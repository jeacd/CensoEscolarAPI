from flask_restful import Resource, marshal
import psycopg2.extras
from flask import request

from models.instituicaoEnsino import InstituicaoEnsino, InstituicaoEnsinoSchema, instituicao_fields

from helpers.database import getConnection
from helpers.logging import logger


class InstituicoesResource(Resource):
    def get(self):
        conn = getConnection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        logger.info("GET Instituições")
        
        # instituicoesEnsino = []

        cur.execute('''
            SELECT * FROM tb_instituicao
        ''')
        resultSet = cur.fetchall()
        
        instituicoesEnsino = [InstituicaoEnsino(**instituicao) for instituicao in resultSet]
        # for instituicao in resultSet:
        #     instituicaoEnsino = InstituicaoEnsino(**instituicao)
        #     instituicoesEnsino.append(instituicaoEnsino)
            
        # schema = InstituicaoEnsinoSchema(many=True)
        
        return marshal(instituicoesEnsino, instituicao_fields), 200
    
    def post(self):
        logger.info("POST Instituição")

        dados = request.get_json()
        schema = InstituicaoEnsinoSchema()

        try:
            dados_validados = schema.load(dados)
        except Exception as e:
            return {"erro": str(e)}, 400

        conn = getConnection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cur.execute("""
            INSERT INTO tb_instituicao (
                ANO, NO_REGIAO, CO_REGIAO, CO_UF,
                CO_MUNICIPIO, CO_MESORREGIAO, CO_MICRORREGIAO,
                NO_ENTIDADE, CO_ENTIDADE,
                QT_MAT_BAS, QT_MAT_INF, QT_MAT_FUND,
                QT_MAT_MED, QT_MAT_EJA, QT_MAT_ESP
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """, (
            dados_validados["ANO"],
            dados_validados["NO_REGIAO"], dados_validados["CO_REGIAO"], dados_validados["CO_UF"],
            dados_validados["CO_MUNICIPIO"], dados_validados["CO_MESORREGIAO"], dados_validados["CO_MICRORREGIAO"],
            dados_validados["NO_ENTIDADE"], dados_validados["CO_ENTIDADE"],
            dados_validados["QT_MAT_BAS"], dados_validados["QT_MAT_INF"], dados_validados["QT_MAT_FUND"],
            dados_validados["QT_MAT_MED"], dados_validados["QT_MAT_EJA"], dados_validados["QT_MAT_ESP"]
        ))

        nova_instituicao = cur.fetchone()
        conn.commit()

        return marshal(InstituicaoEnsino(**nova_instituicao), instituicao_fields), 201
    
class InstituicaoResource(Resource):
    def get(self, id):
        try:
            logger.info(f"GET Instituição pelo Identificador: {id}")

            conn = getConnection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute("""
                SELECT * FROM tb_instituicao WHERE id = %s
            """, (id,))
            resultSet = cur.fetchone()

            if not resultSet:
                logger.error(f"Instituição com o id: {id} não encontrada")
                return {"erro": "Instituição não encontrada"}, 404

            return marshal(InstituicaoEnsino(**resultSet), instituicao_fields), 200

        except Exception as e:
            logger.error(f"GET Instituição por Identificador - Erro: {e}")
            return {"erro": str(e)}, 400
    
    def delete(self, id):
        try:
            logger.info(f"DELETE {id}")
            
            conn = getConnection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute('''
            DELETE FROM tb_instituicao WHERE id = %s
            ''', (id,))
            conn.commit()
            
            return {'mensagem': 'Instituição removida'}, 200
        except:
            logger.info(f'Instituição ({id}) não removida')
            return {'mensagem': 'Instituição não removida'}, 404
    
    def put(self, id):
        logger.info(f"PUT - Atualizar Instituição ID {id}")
        
        schema = InstituicaoEnsinoSchema()
        
        try:
            dados = schema.load(request.get_json())
        except Exception as e:
            return {"erro": str(e)}, 400

        conn = getConnection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cur.execute("""
            UPDATE tb_instituicao
            SET NO_ENTIDADE = %s
            WHERE id = %s
            RETURNING *
        """, (dados["NO_ENTIDADE"], id))
        resultSet = cur.fetchone()
        conn.commit()
        conn.close()

        if not resultSet:
            return {'mensagem': 'Instituição não encontrada'}, 404

        return marshal(InstituicaoEnsino(**resultSet), instituicao_fields), 200