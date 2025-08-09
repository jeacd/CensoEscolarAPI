# class Mesorregiao():
#     def __init__(self, **kwargs):
#         self.id = kwargs.get('id')
#         self.nome = kwargs.get('nome')
#         self.cp_uf = kwargs.get('co_uf')

#     def toDict(self):
#         return self.__dict__

from marshmallow import Schema, fields
from flask_restful import fields as flaskFields

mesorregiao_fields = {
    'id': flaskFields.Integer,
    'nome': flaskFields.String,
    'co_uf': flaskFields.Integer,
}

class Mesorregiao:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.nome = kwargs.get('nome')
        self.co_uf = kwargs.get('co_uf')

class MesorregiaoSchema(Schema):
    id = fields.Int()
    nome = fields.Str()
    co_uf = fields.Int()
