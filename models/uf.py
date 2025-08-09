# class Uf():
#     def __init__(self, **kwargs):
#         self.id = kwargs.get('id')
#         self.sigla = kwargs.get('sigla')
#         self.nome = kwargs.get('nome')

#     def toDict(self):
#         return self.__dict__

from marshmallow import Schema, fields
from flask_restful import fields as flaskFields

uf_fields = {
    'id': flaskFields.Integer,
    'sigla': flaskFields.String,
    'nome': flaskFields.String,
}

class Uf:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.sigla = kwargs.get('sigla')
        self.nome = kwargs.get('nome')

class UfSchema(Schema):
    id = fields.Int()
    sigla = fields.Str()
    nome = fields.Str()