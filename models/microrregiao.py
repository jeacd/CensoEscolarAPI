class Microrregiao():
    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.nome = kwargs.get('nome')
        self.co_uf = kwargs.get('co_uf')

    def toDict(self):
        return self.__dict__

