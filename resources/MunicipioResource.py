from flask_restful import Resource, marshal
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

from helpers.logging import logger
from helpers.database import db
from models.municipio import Municipio, MunicipioSchema, municipio_fields


class MunicipiosResource(Resource):
    def get(self):
        logger.info("GET Municipios")

        try:
            municipios = Municipio.query.all()
            return marshal(municipios, municipio_fields), 200
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar municipios: {e}")
            return {"erro": "Problema com o banco de dados."}, 500

    def post(self):
        logger.info("POST Municipio")

        schema = MunicipioSchema()
        dados = request.get_json()

        try:
            dados_validados = schema.load(dados)
        except ValidationError as e:
            return {"erro": e.messages}, 400

        try:
            municipio = Municipio(**dados_validados)
            db.session.add(municipio)
            db.session.commit()
            return marshal(municipio, municipio_fields), 201
        except SQLAlchemyError as e:
            logger.error(f"Erro ao inserir municipio: {e}")
            db.session.rollback()
            return {"erro": "Erro ao inserir municipio"}, 500


class MunicipioResource(Resource):
    def get(self, id):
        logger.info(f"GET Municipio ID {id}")

        municipio = Municipio.query.get(id)
        if not municipio:
            return {"erro": "Municipio não encontrado"}, 404

        return marshal(municipio, municipio_fields), 200

    def put(self, id):
        logger.info(f"PUT Municipio ID {id}")

        schema = MunicipioSchema()
        dados = request.get_json()

        try:
            dados_validados = schema.load(dados)
        except ValidationError as e:
            return {"erro": e.messages}, 400

        municipio = Municipio.query.get(id)
        if not municipio:
            return {"erro": "Municipio não encontrado"}, 404

        try:
            for key, value in dados_validados.items():
                setattr(municipio, key, value)
            db.session.commit()
            return marshal(municipio, municipio_fields), 200
        except SQLAlchemyError as e:
            logger.error(f"Erro ao atualizar municipio: {e}")
            db.session.rollback()
            return {"erro": "Erro ao atualizar municipio"}, 500

    def delete(self, id):
        logger.info(f"DELETE Municipio ID {id}")

        municipio = Municipio.query.get(id)
        if not municipio:
            return {"erro": "Municipio não encontrado"}, 404

        try:
            db.session.delete(municipio)
            db.session.commit()
            return {"mensagem": "Municipio removido"}, 200
        except SQLAlchemyError as e:
            logger.error(f"Erro ao deletar municipio: {e}")
            db.session.rollback()
            return {"erro": "Erro ao deletar municipio"}, 500
