from flask_restful import Resource, marshal
import psycopg2.extras
from flask import request

from models.mesorregiao import Mesorregiao, MesorregiaoSchema, mesorregiao_fields
from helpers.database import getConnection
from helpers.logging import logger


class MesorregiaoResource(Resource):
    def get(self, id):
        logger.info(f"GET Mesorregiao pelo ID: {id}")

        try:
            conn = getConnection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute("""
                SELECT id, nome, co_uf FROM tb_mesorregiao WHERE id = %s
            """, (id,))
            resultSet = cur.fetchone()
            conn.close()

            if not resultSet:
                logger.error(f"Mesorregiao com id {id} não encontrada")
                return {"erro": "Mesorregiao não encontrada"}, 404

            mesorregiao_obj = Mesorregiao(**resultSet)
            return marshal(mesorregiao_obj, mesorregiao_fields), 200

        except Exception as e:
            logger.error(f"Erro ao buscar Mesorregiao ID {id}: {e}")
            return {"erro": str(e)}, 400

    def put(self, id):
        logger.info(f"PUT - Atualizar Mesorregiao ID {id}")

        schema = MesorregiaoSchema()

        try:
            dados = schema.load(request.get_json())
        except Exception as e:
            return {"erro": str(e)}, 400

        try:
            conn = getConnection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute("""
                UPDATE tb_mesorregiao
                SET nome = %s
                WHERE id = %s
                RETURNING *
            """, (dados["nome"], id))

            resultSet = cur.fetchone()
            conn.commit()

            if not resultSet:
                return {"erro": "Mesorregiao não encontrada"}, 404

            mesorregiao_obj = Mesorregiao(**resultSet)
            return marshal(mesorregiao_obj, mesorregiao_fields), 200

        except Exception as e:
            logger.error(f"Erro ao atualizar Mesorregiao ID {id}: {e}")
            return {"erro": str(e)}, 400

    def delete(self, id):
        logger.info(f"DELETE Mesorregiao ID {id}")

        try:
            conn = getConnection()
            cur = conn.cursor()

            cur.execute("""
                DELETE FROM tb_mesorregiao WHERE id = %s
            """, (id,))
            conn.commit()
            affected = cur.rowcount
            conn.close()

            if affected == 0:
                return {"erro": "Mesorregiao não encontrada"}, 404

            return {"mensagem": "Mesorregiao removida"}, 200

        except Exception as e:
            logger.error(f"Erro ao deletar Mesorregiao ID {id}: {e}")
            return {"erro": str(e)}, 400
        
class MesorregioesResource(Resource):
    def get(self):
        conn = getConnection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        logger.info("GET Mesorregiões")

        cur.execute('''
            SELECT * FROM tb_mesorregiao
        ''')
        resultSet = cur.fetchall()
        
        Mesorregioes = [Mesorregiao(**mesorregiao) for mesorregiao in resultSet]
        
        return marshal(Mesorregioes, mesorregiao_fields), 200
    
    def post(self):
        logger.info("POST Mesorregiao")
        
        dados = request.get_json()
    
        conn = getConnection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        schema = MesorregiaoSchema()

        try:
            dados_validados = schema.load(dados)
        except Exception as e:
            return {"erro": str(e)}, 400
        
        cur.execute('''
            INSERT INTO tb_mesorregiao (
                id, nome, co_uf
            ) VALUES (%s, %s, %s)
            ''',
            (
                dados_validados["id"], dados_validados["nome"], dados_validados["co_uf"]
            )
        )
        conn.commit()
        
        mesorregiao = Mesorregiao(**dados_validados)

        return marshal(mesorregiao, mesorregiao_fields), 201
