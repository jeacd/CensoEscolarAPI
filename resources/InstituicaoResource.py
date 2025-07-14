from flask_restful import Resource, marshal
import psycopg2.extras

from models.instituicaoEnsino import InstituicaoEnsino, InstituicaoEnsinoSchema, instituicao_fields

from helpers.database import getConnection
from helpers.logging import logger


class InstituicoesResource(Resource):
    def get(self):
        conn = getConnection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        
        logger.info("GET Instituições")
        
        instituicoesEnsino = []

        cur.execute('''
            SELECT * FROM tb_instituicao
        ''')
        resultSet = cur.fetchall()
        
        for instituicao in resultSet:
            instituicaoEnsino = InstituicaoEnsino(**instituicao)
            instituicoesEnsino.append(instituicaoEnsino)
            
        schema = InstituicaoEnsinoSchema(many=True)
        return marshal(instituicoesEnsino, instituicao_fields), 200