from flask_restful import Resource

class InstituicaoResource(Resource):
    def get(self):
        return {'Hello': 'World'}