from marshmallow import Schema, fields
from typing import Optional
from sqlalchemy import Integer, String, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from flask_restful import fields as flaskFields

from helpers.database import db

uf_fields = {
    "id": flaskFields.Integer,
    "created": flaskFields.DateTime,
    "sigla": flaskFields.String,
    "nome": flaskFields.String,
}

class UfSchema(Schema):
    id = fields.Int(dump_only=True)
    created = fields.DateTime(dump_only=True)
    sigla = fields.Str(allow_none=True)
    nome = fields.Str(allow_none=True)

class Uf(db.Model):
    __tablename__ = "tb_uf"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    created: Mapped[datetime] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.current_timestamp()
    )
    sigla: Mapped[Optional[str]] = mapped_column(String)
    nome: Mapped[Optional[str]] = mapped_column(String)

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        return f"<Uf id={self.id} sigla={self.sigla} nome={self.nome}>"
