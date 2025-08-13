from flask_restful import Resource
from flask import request
from sqlalchemy.exc import SQLAlchemyError
from helpers.logging import logger
from helpers.database import db
from models.instituicaoEnsino import InstituicaoEnsino

class AnosResource(Resource):
    def get(self):
        try:
            anos = db.session.query(InstituicaoEnsino.ano).distinct().all()
            anos_dict = {str(i): ano[0] for i, ano in enumerate(anos)}
            return anos_dict, 200
        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar anos: {e}")
            return {"erro": "Problema com o banco de dados."}, 500

class MinAndMaxValuesResource(Resource):
    def get(self):
        ano = request.args.get('ano', type=int, default=0)

        if ano <= 0:
            return {'erro': 'Ano inválido'}, 400
        
        try:
            subquery = (
                db.session.query(
                    InstituicaoEnsino.co_uf,
                    db.func.sum(InstituicaoEnsino.qt_mat_bas).label("soma")
                )
                .filter(InstituicaoEnsino.ano == ano)
                .group_by(InstituicaoEnsino.co_uf)
                .subquery()
            )

            resultado = db.session.query(
                db.func.min(subquery.c.soma).label("menor_valor"),
                db.func.max(subquery.c.soma).label("maior_valor")
            ).one()

            if resultado.menor_valor is not None and resultado.maior_valor is not None:
                return {
                    "menor_valor": resultado.menor_valor,
                    "maior_valor": resultado.maior_valor
                }, 200

            return {'erro': 'Nenhum dado encontrado para este ano'}, 404

        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar min/max valores: {e}")
            return {"erro": "Problema com o banco de dados."}, 500

class CensoEscolarResource(Resource):
    def get(self):
        ano = request.args.get('ano', type=int, default=0)
        estado = request.args.get('estado', type=int, default=0)

        if ano == 0:
            return {}, 200

        try:
            query = db.session.query(
                InstituicaoEnsino.co_uf,
                db.func.sum(InstituicaoEnsino.qt_mat_bas).label("qt_mat_bas")
            ).filter(InstituicaoEnsino.ano == ano)

            if estado != 0:
                query = query.filter(InstituicaoEnsino.co_uf == estado)

            query = query.group_by(InstituicaoEnsino.co_uf)

            resultados = query.all()

            return {str(row.co_uf): row.qt_mat_bas for row in resultados}, 200

        except SQLAlchemyError as e:
            logger.error(f"Erro ao buscar dados do censo escolar: {e}")
            return {"erro": "Erro interno no servidor"}, 500
