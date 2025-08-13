from helpers.application import app, api
from helpers.CORS import cors

from resources.IndexResource import IndexResource

from resources.InstituicaoResource import InstituicaoResource
from resources.InstituicaoResource import InstituicoesResource

from resources.InstituicaoAnalyticsResource import AnosResource
from resources.InstituicaoAnalyticsResource import MinAndMaxValuesResource
from resources.InstituicaoAnalyticsResource import CensoEscolarResource

from resources.UfResource import UfResource
from resources.UfResource import UfsResource

from resources.MesorregiaoResource import MesorregioesResource
from resources.MesorregiaoResource import MesorregiaoResource

from resources.MunicipioResource import MunicipiosResource
from resources.MunicipioResource import MunicipioResource

from resources.MicrorregiaoResource import MicrorregioesResource
from resources.MicrorregiaoResource import MicrorregiaoResource


cors.init_app(app)


api.add_resource(IndexResource, '/')
api.add_resource(InstituicaoResource, '/instituicaoensino/<int:id>')
api.add_resource(InstituicoesResource, '/instituicoesensino')

api.add_resource(AnosResource, '/anos')
api.add_resource(MinAndMaxValuesResource, '/minandmaxvalues')
api.add_resource(CensoEscolarResource, '/censoescolar')

api.add_resource(UfResource, '/estado/<int:id>')
api.add_resource(UfsResource, '/estados')

api.add_resource(MesorregiaoResource, '/mesorregiao/<int:id>')
api.add_resource(MesorregioesResource, '/mesorregioes')

api.add_resource(MunicipioResource, '/municipio/<int:id>')
api.add_resource(MunicipiosResource, '/municipios')

api.add_resource(MicrorregiaoResource, '/microrregiao/<int:id>')
api.add_resource(MicrorregioesResource, '/microrregioes')


if __name__ == '__main__':
    app.run()

