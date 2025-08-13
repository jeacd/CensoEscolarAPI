from flask_restful import Resource, marshal
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

from helpers.logging import logger
from helpers.database import db
from models.uf import Uf, UfSchema, uf_fields


class UfsResource(Resource):
    def get(self):
        logger.info("GET UFs")

        try:
            ufs = Uf.query.all()
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar UFs: {e}")
            return {"erro": "Problema com o banco de dados."}, 500

        return marshal(ufs, uf_fields), 200

    def post(self):
        logger.info("POST UF")

        schema = UfSchema()
        dados = request.get_json()

        try:
            dados_validados = schema.load(dados)
        except ValidationError as e:
            return {"erro": e.messages}, 400

        try:
            uf = Uf(**dados_validados)
            db.session.add(uf)
            db.session.commit()
            return marshal(uf, uf_fields), 201
        except SQLAlchemyError as e:
            logger.error(f"Erro ao inserir UF: {e}")
            db.session.rollback()
            return {"erro": "Erro ao inserir UF"}, 500


class UfResource(Resource):
    def get(self, id):
        logger.info(f"GET UF ID {id}")

        uf = Uf.query.get(id)
        if not uf:
            return {"erro": "UF não encontrada"}, 404

        return marshal(uf, uf_fields), 200

    def put(self, id):
        logger.info(f"PUT UF ID {id}")

        schema = UfSchema()
        dados = request.get_json()

        try:
            dados_validados = schema.load(dados)
        except ValidationError as e:
            return {"erro": e.messages}, 400

        uf = Uf.query.get(id)
        if not uf:
            return {"erro": "UF não encontrada"}, 404

        try:
            for key, value in dados_validados.items():
                setattr(uf, key, value)
            db.session.commit()
            return marshal(uf, uf_fields), 200
        except SQLAlchemyError as e:
            logger.error(f"Erro ao atualizar UF: {e}")
            db.session.rollback()
            return {"erro": "Erro ao atualizar UF"}, 500

    def delete(self, id):
        logger.info(f"DELETE UF ID {id}")

        uf = Uf.query.get(id)
        if not uf:
            return {"erro": "UF não encontrada"}, 404

        try:
            db.session.delete(uf)
            db.session.commit()
            return {"mensagem": "UF removida"}, 200
        except SQLAlchemyError as e:
            logger.error(f"Erro ao deletar UF: {e}")
            db.session.rollback()
            return {"erro": "Erro ao deletar UF"}, 500
