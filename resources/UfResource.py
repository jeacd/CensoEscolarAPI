from flask_restful import Resource, marshal
import psycopg2.extras
from flask import request

from models.uf import Uf, UfSchema, uf_fields
from helpers.database import getConnection
from helpers.logging import logger


class UfsResource(Resource):
    def get(self):
        logger.info("GET Estados (UFs)")

        conn = getConnection()
        cur = conn.cursor()
        cur.execute('SELECT id, nome FROM tb_uf')
        resultSet = cur.fetchall()
        
        dict_result = {str(id): nome for id, nome in resultSet}

        return dict_result, 200

    def post(self):
        logger.info("POST UF")

        dados = request.get_json()
        schema = UfSchema()

        try:
            dados_validados = schema.load(dados)
        except Exception as e:
            return {"erro": str(e)}, 400

        uf_obj = Uf(**dados_validados)

        conn = getConnection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cur.execute('''
            INSERT INTO tb_uf (
                id, sigla, nome
            ) VALUES (%s, %s, %s)
            RETURNING *
        ''', (
            uf_obj.id,
            uf_obj.sigla,
            uf_obj.nome
        ))

        resultSet = cur.fetchone()
        conn.commit()

        uf_obj = Uf(**resultSet)

        return marshal(uf_obj, uf_fields), 201


class UfResource(Resource):
    def get(self, id):
        try:
            logger.info(f"GET UF pelo ID: {id}")

            conn = getConnection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute("""
                SELECT id, sigla, nome FROM tb_uf WHERE id = %s
            """, (id,))
            resultSet = cur.fetchone()

            if not resultSet:
                logger.error(f"UF com id: {id} não encontrada")
                return {"erro": "UF não encontrada"}, 404

            uf_obj = Uf(**resultSet)

            return marshal(uf_obj, uf_fields), 200

        except Exception as e:
            logger.error(f"Erro ao buscar UF ID {id}: {e}")
            return {"erro": str(e)}, 400

    def delete(self, id):
        try:
            logger.info(f"DELETE UF ID {id}")

            conn = getConnection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute('''
                DELETE FROM tb_uf WHERE id = %s
            ''', (id,))
            conn.commit()

            if cur.rowcount == 0:
                return {'mensagem': 'UF não encontrada'}, 404

            return {'mensagem': 'UF removida'}, 200

        except Exception as e:
            logger.error(f"Erro ao deletar UF ID {id}: {e}")
            return {'mensagem': 'UF não removida', 'erro': str(e)}, 400

    def put(self, id):
        logger.info(f"PUT - Atualizar UF ID {id}")

        schema = UfSchema()

        try:
            dados = schema.load(request.get_json())
        except Exception as e:
            return {"erro": str(e)}, 400

        uf_obj = Uf(**dados)

        conn = getConnection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        cur.execute("""
            UPDATE tb_uf
            SET sigla = %s, nome = %s
            WHERE id = %s
            RETURNING *
        """, (
            uf_obj.sigla,
            uf_obj.nome,
            id
        ))
        resultSet = cur.fetchone()
        conn.commit()

        if not resultSet:
            return {'mensagem': 'UF não encontrada'}, 404

        uf_obj = Uf(**resultSet)

        return marshal(uf_obj, uf_fields), 200
