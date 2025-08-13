from marshmallow import Schema, fields
from typing import Optional
from sqlalchemy import Integer, String, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from flask_restful import fields as flaskFields

from helpers.database import db

microrregiao_fields = {
    "id": flaskFields.Integer,
    "created": flaskFields.DateTime,
    "nome": flaskFields.String,
    "co_uf": flaskFields.Integer,
}

class MicrorregiaoSchema(Schema):
    id = fields.Int(dump_only=True)
    created = fields.DateTime(dump_only=True)
    nome = fields.Str(allow_none=True)
    co_uf = fields.Int(allow_none=True)

class Microrregiao(db.Model):
    __tablename__ = "tb_microrregiao"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.current_timestamp()
    )
    nome: Mapped[Optional[str]] = mapped_column(String)
    co_uf: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("tb_uf.id"))

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"<Microrregiao id={self.id} nome={self.nome}>"
