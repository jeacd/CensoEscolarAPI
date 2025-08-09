# class Municipio():
#     def __init__(self, **kwargs):
#         self.id = kwargs.get('id')
#         self.nome = kwargs.get('nome')
#         self.co_uf = kwargs.get('co_uf')
#         self.co_mesorregiao = kwargs.get('co_mesorregiao')
#         self.co_microrregiao = kwargs.get('co_microrregiao')

#     def toDict(self):
#         return self.__dict__

from marshmallow import Schema, fields
from flask_restful import fields as flaskFields

municipio_fields = {
    'id': flaskFields.Integer,
    'nome': flaskFields.String,
    'co_uf': flaskFields.Integer,
    'co_mesorregiao': flaskFields.Integer,
    'co_microrregiao': flaskFields.Integer,
}

class Municipio:
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.nome = kwargs.get('nome')
        self.co_uf = kwargs.get('co_uf')
        self.co_mesorregiao = kwargs.get('co_mesorregiao')
        self.co_microrregiao = kwargs.get('co_microrregiao')

class MunicipioSchema(Schema):
    id = fields.Int()
    nome = fields.Str()
    co_uf = fields.Int()
    co_mesorregiao = fields.Int()
    co_microrregiao = fields.Int()
