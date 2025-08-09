from flask_restful import Resource
from flask import request, jsonify
import psycopg2.extras

from helpers.database import getConnection
from helpers.logging import logger

class AnosResource(Resource):
    def get(self):
        conn = getConnection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        cur.execute('''
            SELECT DISTINCT ano FROM tb_instituicao
        ''')
        resultSet = cur.fetchall()
        
        anos = {str(i): resultSet[i]['ano'] for i in range(len(resultSet))}
        
        return anos, 200
    
class MinAndMaxValuesResource(Resource):
    def get(self):
        ano = int(request.args.get('ano', 0))

        conn = getConnection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        if ano > 0:
            cur.execute('''
                SELECT 
                    MIN(soma) AS menor_valor, 
                    MAX(soma) AS maior_valor
                FROM (
                    SELECT SUM(qt_mat_bas) AS soma
                    FROM tb_instituicao
                    WHERE ano = %s
                    GROUP BY co_uf
                ) AS sub
            ''', (ano,))
            resultSet = cur.fetchone()

            if resultSet and (resultSet['menor_valor'] is not None and resultSet['maior_valor'] is not None):
                return resultSet, 200

            return {'erro': 'Nenhum dado encontrado para este ano'}, 404

        return {'erro': 'Ano inválido'}, 400
    
class CensoEscolarResource(Resource):
    def get(self):
        ano = int(request.args.get('ano', 0))
        estado = int(request.args.get('estado', 0))

        if ano == 0:
            return {}, 200

        conn = getConnection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        try:
            if estado == 0:
                cur.execute('''
                    SELECT co_uf, SUM(qt_mat_bas) as qt_mat_bas
                    FROM tb_instituicao
                    WHERE ano = %s
                    GROUP BY co_uf
                ''', (ano,))
            else:
                cur.execute('''
                    SELECT co_uf, SUM(qt_mat_bas) as qt_mat_bas
                    FROM tb_instituicao
                    WHERE ano = %s AND co_uf = %s
                    GROUP BY co_uf
                ''', (ano, estado))

            result_set = cur.fetchall()
            return {str(row["co_uf"]): row["qt_mat_bas"] for row in result_set}, 200

        except Exception as e:
            logger.error(f"Erro ao buscar dados do censo escolar: {e}")
            return {"erro": "Erro interno no servidor"}, 500