class Uf():
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.sigla = kwargs.get('sigla')
        self.nome = kwargs.get('nome')

    def toDict(self):
        return self.__dict__

