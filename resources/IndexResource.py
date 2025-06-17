from flask_restful import Resource

class IndexResource(Resource):
    def get(self):
        versao = {'Versão': '2.3.8'}
        return versao, 200