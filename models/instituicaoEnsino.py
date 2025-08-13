from marshmallow import Schema, fields
from typing import Optional
from sqlalchemy import Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from flask_restful import fields as flaskFields

from helpers.database import db

instituicao_fields = {
    "id": flaskFields.Integer,
    "created": flaskFields.DateTime,
    "ano": flaskFields.Integer,
    "no_regiao": flaskFields.String,
    "co_regiao": flaskFields.Integer,
    "co_uf": flaskFields.Integer,
    "co_municipio": flaskFields.Integer,
    "co_mesorregiao": flaskFields.Integer,
    "co_microrregiao": flaskFields.Integer,
    "no_entidade": flaskFields.String,
    "co_entidade": flaskFields.Integer,
    "qt_mat_bas": flaskFields.Integer,
    "qt_mat_inf": flaskFields.Integer,
    "qt_mat_fund": flaskFields.Integer,
    "qt_mat_med": flaskFields.Integer,
    "qt_mat_eja": flaskFields.Integer,
    "qt_mat_esp": flaskFields.Integer,
}

class InstituicaoEnsinoSchema(Schema):
    id = fields.Int(dump_only=True)
    ano = fields.Int(allow_none=True)
    no_regiao = fields.Str(allow_none=True)
    co_regiao = fields.Int(allow_none=True)
    co_uf = fields.Int(allow_none=True)
    co_municipio = fields.Int(allow_none=True)
    co_mesorregiao = fields.Int(allow_none=True)
    co_microrregiao = fields.Int(allow_none=True)
    no_entidade = fields.Str(allow_none=True)
    co_entidade = fields.Int(allow_none=True)
    qt_mat_bas = fields.Int(allow_none=True)
    qt_mat_inf = fields.Int(allow_none=True)
    qt_mat_fund = fields.Int(allow_none=True)
    qt_mat_med = fields.Int(allow_none=True)
    qt_mat_eja = fields.Int(allow_none=True)
    qt_mat_esp = fields.Int(allow_none=True)

class InstituicaoEnsino(db.Model):
    __tablename__ = "tb_instituicao"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.current_timestamp()
    )
    ano: Mapped[Optional[int]] = mapped_column(Integer)
    no_regiao: Mapped[Optional[str]] = mapped_column(String)
    co_regiao: Mapped[Optional[int]] = mapped_column(Integer)

    co_uf: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("tb_uf.id"))
    co_municipio: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("tb_municipio.id"))
    co_mesorregiao: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("tb_mesorregiao.id"))
    co_microrregiao: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("tb_microrregiao.id"))

    no_entidade: Mapped[Optional[str]] = mapped_column(String)
    co_entidade: Mapped[Optional[int]] = mapped_column(Integer)
    qt_mat_bas: Mapped[Optional[int]] = mapped_column(Integer)
    qt_mat_inf: Mapped[Optional[int]] = mapped_column(Integer)
    qt_mat_fund: Mapped[Optional[int]] = mapped_column(Integer)
    qt_mat_med: Mapped[Optional[int]] = mapped_column(Integer)
    qt_mat_eja: Mapped[Optional[int]] = mapped_column(Integer)
    qt_mat_esp: Mapped[Optional[int]] = mapped_column(Integer)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"<InstituicaoEnsino id={self.id} no_entidade={self.no_entidade}>"
