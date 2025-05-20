class Municipio():
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.nome = kwargs.get('nome')
        self.co_uf = kwargs.get('co_uf')
        self.co_mesorregiao = kwargs.get('co_mesorregiao')
        self.co_microrregiao = kwargs.get('co_microrregiao')

    def toDict(self):
        return self.__dict__

