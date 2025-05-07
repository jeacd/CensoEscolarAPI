class InstituicaoEnsino():
    def __init__(
        self, id,
        NO_REGIAO, CO_REGIAO, NO_UF, CO_UF,
        NO_MUNICIPIO, CO_MUNICIPIO,
        NO_MESORREGIAO, CO_MESORREGIAO,
        NO_MICRORREGIAO, CO_MICRORREGIAO,
        NO_ENTIDADE, CO_ENTIDADE,
        QT_MAT_BAS, QT_MAT_INF, QT_MAT_FUND,
        QT_MAT_MED, QT_MAT_EJA, QT_MAT_ESP
    ):
        self.id = id
        self.NO_REGIAO = NO_REGIAO
        self.CO_REGIAO = CO_REGIAO
        self.NO_UF = NO_UF
        self.CO_UF = CO_UF
        self.NO_MUNICIPIO = NO_MUNICIPIO
        self.CO_MUNICIPIO = CO_MUNICIPIO
        self.NO_MESORREGIAO = NO_MESORREGIAO
        self.CO_MESORREGIAO = CO_MESORREGIAO
        self.NO_MICRORREGIAO = NO_MICRORREGIAO
        self.CO_MICRORREGIAO = CO_MICRORREGIAO
        self.NO_ENTIDADE = NO_ENTIDADE
        self.CO_ENTIDADE = CO_ENTIDADE
        self.QT_MAT_BAS = QT_MAT_BAS
        self.QT_MAT_INF = QT_MAT_INF
        self.QT_MAT_FUND = QT_MAT_FUND
        self.QT_MAT_MED = QT_MAT_MED
        self.QT_MAT_EJA = QT_MAT_EJA
        self.QT_MAT_ESP = QT_MAT_ESP

    def toDict(self):
        return {
            'id': self.id,
            'NO_REGIAO': self.NO_REGIAO,
            'CO_REGIAO': self.CO_REGIAO,
            'NO_UF': self.NO_UF,
            'CO_UF': self.CO_UF,
            'NO_MUNICIPIO': self.NO_MUNICIPIO,
            'CO_MUNICIPIO': self.CO_MUNICIPIO,
            'NO_MESORREGIAO': self.NO_MESORREGIAO,
            'CO_MESORREGIAO': self.CO_MESORREGIAO,
            'NO_MICRORREGIAO': self.NO_MICRORREGIAO,
            'CO_MICRORREGIAO': self.CO_MICRORREGIAO,
            'NO_ENTIDADE': self.NO_ENTIDADE,
            'CO_ENTIDADE': self.CO_ENTIDADE,
            'QT_MAT_BAS': self.QT_MAT_BAS,
            'QT_MAT_INF': self.QT_MAT_INF,
            'QT_MAT_FUND': self.QT_MAT_FUND,
            'QT_MAT_MED': self.QT_MAT_MED,
            'QT_MAT_EJA': self.QT_MAT_EJA,
            'QT_MAT_ESP': self.QT_MAT_ESP
        }

