from flask_restful import Resource, marshal
import psycopg2.extras
from flask import request

from models.microrregiao import Microrregiao, MicrorregiaoSchema, microrregiao_fields
from helpers.database import getConnection
from helpers.logging import logger


class MicrorregioesResource(Resource):
    def get(self):
        logger.info("GET todas Microrregioes")

        try:
            conn = getConnection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute("SELECT id, nome, co_uf FROM tb_microrregiao")
            resultSet = cur.fetchall()

            microrregioes = [Microrregiao(**microrregiao) for microrregiao in resultSet]
            return marshal(microrregioes, microrregiao_fields), 200

        except Exception as e:
            logger.error(f"Erro ao buscar Microrregioes: {e}")
            return {"erro": str(e)}, 400

    def post(self):
        logger.info("POST Microrregiao")

        dados = request.get_json()
        schema = MicrorregiaoSchema()

        try:
            dados_validados = schema.load(dados)
        except Exception as e:
            return {"erro": str(e)}, 400

        try:
            conn = getConnection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute("""
                INSERT INTO tb_microrregiao (id, nome, co_uf)
                VALUES (%s, %s, %s)
                RETURNING *
            """, (
                dados_validados["id"],
                dados_validados["nome"],
                dados_validados["co_uf"]
            ))

            resultSet = cur.fetchone()
            conn.commit()

            microrregiao_obj = Microrregiao(**resultSet)
            return marshal(microrregiao_obj, microrregiao_fields), 201

        except Exception as e:
            logger.error(f"Erro ao inserir Microrregiao: {e}")
            return {"erro": str(e)}, 400


class MicrorregiaoResource(Resource):
    def get(self, id):
        logger.info(f"GET Microrregiao pelo ID: {id}")

        try:
            conn = getConnection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute("""
                SELECT id, nome, co_uf FROM tb_microrregiao WHERE id = %s
            """, (id,))
            resultSet = cur.fetchone()

            if not resultSet:
                logger.error(f"Microrregiao com id {id} não encontrada")
                return {"erro": "Microrregiao não encontrada"}, 404

            microrregiao_obj = Microrregiao(**resultSet)
            return marshal(microrregiao_obj, microrregiao_fields), 200

        except Exception as e:
            logger.error(f"Erro ao buscar Microrregiao ID {id}: {e}")
            return {"erro": str(e)}, 400

    def put(self, id):
        logger.info(f"PUT - Atualizar Microrregiao ID {id}")

        schema = MicrorregiaoSchema()

        try:
            dados = schema.load(request.get_json())
        except Exception as e:
            return {"erro": str(e)}, 400

        try:
            conn = getConnection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute("""
                UPDATE tb_microrregiao
                SET nome = %s
                WHERE id = %s
                RETURNING *
            """, (
                dados["nome"],
                id
            ))

            resultSet = cur.fetchone()
            conn.commit()

            if not resultSet:
                return {"erro": "Microrregiao não encontrada"}, 404

            microrregiao_obj = Microrregiao(**resultSet)
            return marshal(microrregiao_obj, microrregiao_fields), 200

        except Exception as e:
            logger.error(f"Erro ao atualizar Microrregiao ID {id}: {e}")
            return {"erro": str(e)}, 400

    def delete(self, id):
        logger.info(f"DELETE Microrregiao ID {id}")

        try:
            conn = getConnection()
            cur = conn.cursor()

            cur.execute("""
                DELETE FROM tb_microrregiao WHERE id = %s
            """, (id,))
            conn.commit()

            if cur.rowcount == 0:
                return {"erro": "Microrregiao não encontrada"}, 404

            return {"mensagem": "Microrregiao removida"}, 200

        except Exception as e:
            logger.error(f"Erro ao deletar Microrregiao ID {id}: {e}")
            return {"erro": str(e)}, 400
