from marshmallow import Schema, fields
from flask_restful import fields as flaskFields

instituicao_fields = {
    'id':   flaskFields.Integer,
    'ANO':   flaskFields.Integer,
    'NO_REGIAO':   flaskFields.String,
    'CO_REGIAO':   flaskFields.Integer,
    'CO_UF':   flaskFields.Integer,
    'CO_MUNICIPIO':   flaskFields.Integer,
    'CO_MESORREGIAO':   flaskFields.Integer,
    'CO_MICRORREGIAO':   flaskFields.Integer,
    'NO_ENTIDADE':   flaskFields.String,
    'CO_ENTIDADE':   flaskFields.Integer,
    'QT_MAT_BAS':   flaskFields.Integer,
    'QT_MAT_INF':   flaskFields.Integer,
    'QT_MAT_FUND':   flaskFields.Integer,
    'QT_MAT_MED':   flaskFields.Integer,
    'QT_MAT_EJA':   flaskFields.Integer,
    'QT_MAT_ESP':   flaskFields.Integer,
}

class InstituicaoEnsino():
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.ANO = kwargs.get('ano')
        self.NO_REGIAO = kwargs.get('no_regiao')
        self.CO_REGIAO = kwargs.get('co_regiao')
        self.CO_UF = kwargs.get('co_uf')
        self.CO_MUNICIPIO = kwargs.get('co_municipio')
        self.CO_MESORREGIAO = kwargs.get('co_mesorregiao')
        self.CO_MICRORREGIAO = kwargs.get('co_microrregiao')
        self.NO_ENTIDADE = kwargs.get('no_entidade')
        self.CO_ENTIDADE = kwargs.get('co_entidade')
        self.QT_MAT_BAS = kwargs.get('qt_mat_bas')
        self.QT_MAT_INF = kwargs.get('qt_mat_inf')
        self.QT_MAT_FUND = kwargs.get('qt_mat_fund')
        self.QT_MAT_MED = kwargs.get('qt_mat_med')
        self.QT_MAT_EJA = kwargs.get('qt_mat_eja')
        self.QT_MAT_ESP = kwargs.get('qt_mat_esp')
        
class InstituicaoEnsinoSchema(Schema):
    id = fields.Int()
    ANO = fields.Int()
    NO_REGIAO = fields.Str()
    CO_REGIAO = fields.Int()
    CO_UF = fields.Int()
    CO_MUNICIPIO = fields.Int()
    CO_MESORREGIAO = fields.Int()
    CO_MICRORREGIAO = fields.Int()
    NO_ENTIDADE = fields.Str()
    CO_ENTIDADE = fields.Int()
    QT_MAT_BAS = fields.Int()
    QT_MAT_INF = fields.Int()
    QT_MAT_FUND = fields.Int()
    QT_MAT_MED = fields.Int()
    QT_MAT_EJA = fields.Int()
    QT_MAT_ESP = fields.Int()