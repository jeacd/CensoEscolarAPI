from flask_restful import Resource, marshal
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

from helpers.logging import logger
from helpers.database import db
from models.microrregiao import Microrregiao, MicrorregiaoSchema, microrregiao_fields


class MicrorregioesResource(Resource):
    def get(self):
        logger.info("GET todas Microrregiões")

        try:
            microrregioes = Microrregiao.query.all()
            return marshal(microrregioes, microrregiao_fields), 200
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar microrregiões: {e}")
            return {"erro": "Problema ao acessar o banco de dados."}, 500

    def post(self):
        logger.info("POST Microrregião")

        schema = MicrorregiaoSchema()
        dados = request.get_json()

        try:
            dados_validados = schema.load(dados)
        except ValidationError as e:
            return {"erro": e.messages}, 400

        try:
            microrregiao = Microrregiao(**dados_validados)
            db.session.add(microrregiao)
            db.session.commit()
            return marshal(microrregiao, microrregiao_fields), 201
        except SQLAlchemyError as e:
            logger.error(f"Erro ao inserir microrregião: {e}")
            db.session.rollback()
            return {"erro": "Erro ao inserir microrregião"}, 500


class MicrorregiaoResource(Resource):
    def get(self, id):
        logger.info(f"GET Microrregião ID {id}")

        microrregiao = Microrregiao.query.get(id)
        if not microrregiao:
            return {"erro": "Microrregião não encontrada"}, 404

        return marshal(microrregiao, microrregiao_fields), 200

    def put(self, id):
        logger.info(f"PUT Microrregião ID {id}")

        schema = MicrorregiaoSchema()
        dados = request.get_json()

        try:
            dados_validados = schema.load(dados)
        except ValidationError as e:
            return {"erro": e.messages}, 400

        microrregiao = Microrregiao.query.get(id)
        if not microrregiao:
            return {"erro": "Microrregião não encontrada"}, 404

        try:
            for key, value in dados_validados.items():
                setattr(microrregiao, key, value)
            db.session.commit()
            return marshal(microrregiao, microrregiao_fields), 200
        except SQLAlchemyError as e:
            logger.error(f"Erro ao atualizar microrregião: {e}")
            db.session.rollback()
            return {"erro": "Erro ao atualizar microrregião"}, 500

    def delete(self, id):
        logger.info(f"DELETE Microrregião ID {id}")

        microrregiao = Microrregiao.query.get(id)
        if not microrregiao:
            return {"erro": "Microrregião não encontrada"}, 404

        try:
            db.session.delete(microrregiao)
            db.session.commit()
            return {"mensagem": "Microrregião removida"}, 200
        except SQLAlchemyError as e:
            logger.error(f"Erro ao deletar microrregião: {e}")
            db.session.rollback()
            return {"erro": "Erro ao deletar microrregião"}, 500
