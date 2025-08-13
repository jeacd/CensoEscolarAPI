from flask_restful import Resource, marshal
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError

from helpers.logging import logger
from helpers.database import db
from models.instituicaoEnsino import InstituicaoEnsino, InstituicaoEnsinoSchema, instituicao_fields


class InstituicoesResource(Resource):
    def get(self):
        logger.info("GET Instituições")

        try:
            instituicoes = InstituicaoEnsino.query.all()
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar instituições: {e}")
            return {"erro": "Problema com o banco de dados."}, 500

        return marshal(instituicoes, instituicao_fields), 200

    def post(self):
        logger.info("POST Instituição")

        schema = InstituicaoEnsinoSchema()
        dados = request.get_json()

        try:
            dados_validados = schema.load(dados)
        except ValidationError as e:
            return {"erro": e.messages}, 400

        try:
            instituicao = InstituicaoEnsino(**dados_validados)
            db.session.add(instituicao)
            db.session.commit()
            return marshal(instituicao, instituicao_fields), 201
        except SQLAlchemyError as e:
            logger.error(f"Erro ao inserir instituição: {e}")
            db.session.rollback()
            return {"erro": "Erro ao inserir instituição"}, 500


class InstituicaoResource(Resource):
    def get(self, id):
        logger.info(f"GET Instituição ID {id}")

        instituicao = InstituicaoEnsino.query.get(id)
        if not instituicao:
            return {"erro": "Instituição não encontrada"}, 404

        return marshal(instituicao, instituicao_fields), 200

    def put(self, id):
        logger.info(f"PUT Instituição ID {id}")

        schema = InstituicaoEnsinoSchema()
        dados = request.get_json()

        try:
            dados_validados = schema.load(dados)
        except ValidationError as e:
            return {"erro": e.messages}, 400

        instituicao = InstituicaoEnsino.query.get(id)
        if not instituicao:
            return {"erro": "Instituição não encontrada"}, 404

        try:
            for key, value in dados_validados.items():
                setattr(instituicao, key, value)
            db.session.commit()
            return marshal(instituicao, instituicao_fields), 200
        except SQLAlchemyError as e:
            logger.error(f"Erro ao atualizar instituição: {e}")
            db.session.rollback()
            return {"erro": "Erro ao atualizar instituição"}, 500

    def delete(self, id):
        logger.info(f"DELETE Instituição ID {id}")

        instituicao = InstituicaoEnsino.query.get(id)
        if not instituicao:
            return {"erro": "Instituição não encontrada"}, 404

        try:
            db.session.delete(instituicao)
            db.session.commit()
            return {"mensagem": "Instituição removida"}, 200
        except SQLAlchemyError as e:
            logger.error(f"Erro ao deletar instituição: {e}")
            db.session.rollback()
            return {"erro": "Erro ao deletar instituição"}, 500
