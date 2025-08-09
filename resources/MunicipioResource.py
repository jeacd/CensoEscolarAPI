from flask_restful import Resource, marshal
import psycopg2.extras
from flask import request

from models.municipio import Municipio, MunicipioSchema, municipio_fields
from helpers.database import getConnection
from helpers.logging import logger


class MunicipioResource(Resource):
    def get(self, id):
        logger.info(f"GET Municipio pelo ID: {id}")

        try:
            conn = getConnection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute("""
                SELECT id, nome, co_uf, co_mesorregiao, co_microrregiao 
                FROM tb_municipio
                WHERE id = %s
            """, (id,))
            resultSet = cur.fetchone()

            if not resultSet:
                logger.error(f"Municipio com id {id} não encontrado")
                return {"erro": "Municipio não encontrado"}, 404

            municipio_obj = Municipio(**resultSet)
            return marshal(municipio_obj, municipio_fields), 200

        except Exception as e:
            logger.error(f"Erro ao buscar Municipio ID {id}: {e}")
            return {"erro": str(e)}, 400

    def put(self, id):
        logger.info(f"PUT - Atualizar Municipio ID {id}")

        schema = MunicipioSchema()

        try:
            dados = schema.load(request.get_json())
        except Exception as e:
            return {"erro": str(e)}, 400

        try:
            conn = getConnection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute("""
                UPDATE tb_municipio
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
                return {"erro": "Municipio não encontrado"}, 404

            municipio_obj = Municipio(**resultSet)
            
            return marshal(municipio_obj, municipio_fields), 200

        except Exception as e:
            logger.error(f"Erro ao atualizar Municipio ID {id}: {e}")
            return {"erro": str(e)}, 400

    def delete(self, id):
        logger.info(f"DELETE Municipio ID {id}")

        try:
            conn = getConnection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute("""
                DELETE FROM tb_municipio WHERE id = %s
            """, (id,))
            conn.commit()

            if cur.rowcount == 0:
                return {"erro": "Municipio não encontrado"}, 404

            return {"mensagem": "Municipio removido"}, 200

        except Exception as e:
            logger.error(f"Erro ao deletar Municipio ID {id}: {e}")
            return {"erro": str(e)}, 400

class MunicipiosResource(Resource):
    def get(self):
        conn = getConnection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        # logger.info("GET Municipios")

        cur.execute('''
            SELECT * FROM tb_municipio
        ''')
        resultSet = cur.fetchall()
        
        Municipios = [Municipio(**municipio) for municipio in resultSet]
        
        return marshal(Municipios, municipio_fields), 200
    
    def post(self):
        logger.info("POST Municipio")

        dados = request.get_json()
        schema = MunicipioSchema()

        try:
            dados_validados = schema.load(dados)
        except Exception as e:
            return {"erro": str(e)}, 400

        try:
            conn = getConnection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute('''
                INSERT INTO tb_municipio (
                    id, nome, co_uf, co_mesorregiao, co_microrregiao
                ) VALUES (%s, %s, %s, %s, %s)
                RETURNING *
            ''', (
                dados_validados["id"],
                dados_validados["nome"],
                dados_validados["co_uf"],
                dados_validados["co_mesorregiao"],
                dados_validados["co_microrregiao"]
            ))

            resultSet = cur.fetchone()
            conn.commit()

            municipio_obj = Municipio(**resultSet)
            
            return marshal(municipio_obj, municipio_fields), 201

        except Exception as e:
            logger.error(f"Erro ao inserir Municipio: {e}")
            return {"erro": str(e)}, 400