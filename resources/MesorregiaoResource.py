from flask_restful import Resource, marshal
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

from helpers.logging import logger
from helpers.database import db
from models.mesorregiao import Mesorregiao, MesorregiaoSchema, mesorregiao_fields


class MesorregioesResource(Resource):
    def get(self):
        logger.info("GET Mesorregiões")

        try:
            mesorregioes = Mesorregiao.query.all()
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar mesorregiões: {e}")
            return {"erro": "Problema com o banco de dados."}, 500

        return marshal(mesorregioes, mesorregiao_fields), 200

    def post(self):
        logger.info("POST Mesorregião")

        schema = MesorregiaoSchema()
        dados = request.get_json()

        try:
            dados_validados = schema.load(dados)
        except ValidationError as e:
            return {"erro": e.messages}, 400

        try:
            mesorregiao = Mesorregiao(**dados_validados)
            db.session.add(mesorregiao)
            db.session.commit()
            return marshal(mesorregiao, mesorregiao_fields), 201
        except SQLAlchemyError as e:
            logger.error(f"Erro ao inserir mesorregião: {e}")
            db.session.rollback()
            return {"erro": "Erro ao inserir mesorregião"}, 500


class MesorregiaoResource(Resource):
    def get(self, id):
        logger.info(f"GET Mesorregião ID {id}")

        mesorregiao = Mesorregiao.query.get(id)
        if not mesorregiao:
            return {"erro": "Mesorregião não encontrada"}, 404

        return marshal(mesorregiao, mesorregiao_fields), 200

    def put(self, id):
        logger.info(f"PUT Mesorregião ID {id}")

        schema = MesorregiaoSchema()
        dados = request.get_json()

        try:
            dados_validados = schema.load(dados)
        except ValidationError as e:
            return {"erro": e.messages}, 400

        mesorregiao = Mesorregiao.query.get(id)
        if not mesorregiao:
            return {"erro": "Mesorregião não encontrada"}, 404

        try:
            for key, value in dados_validados.items():
                setattr(mesorregiao, key, value)
            db.session.commit()
            return marshal(mesorregiao, mesorregiao_fields), 200
        except SQLAlchemyError as e:
            logger.error(f"Erro ao atualizar mesorregião: {e}")
            db.session.rollback()
            return {"erro": "Erro ao atualizar mesorregião"}, 500

    def delete(self, id):
        logger.info(f"DELETE Mesorregião ID {id}")

        mesorregiao = Mesorregiao.query.get(id)
        if not mesorregiao:
            return {"erro": "Mesorregião não encontrada"}, 404

        try:
            db.session.delete(mesorregiao)
            db.session.commit()
            return {"mensagem": "Mesorregião removida"}, 200
        except SQLAlchemyError as e:
            logger.error(f"Erro ao deletar mesorregião: {e}")
            db.session.rollback()
            return {"erro": "Erro ao deletar mesorregião"}, 500
