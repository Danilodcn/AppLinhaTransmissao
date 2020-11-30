from collections import namedtuple
from math import log, pi as PI, sqrt, hypot

try:
    from .dados import NOMES_CONSTANTES
except ImportError:
    from dados import NOMES_CONSTANTES


def media_geometrica(*args):
    r = 1
    for i in args: r *= i
    return pow(r, 1 / len(args))


class Calculos(object):

    def __init__(self, constantes: list, distancias: list):
        distancias = list(distancias)
        #print("passou", constantes, distancias)

        self.distancias = distancias
        self.constantes = constantes
        tipo = constantes[0]
        nomes_constantes = NOMES_CONSTANTES
        self.Cria_Dados = namedtuple(f"Circuito_{tipo}".title(), nomes_constantes[tipo])
        self.dados = constantes
        self.tipo = self.dados.TIPO
        self.permeabilidade = None
        self.permissividade = None

    @property
    def dados(self):
        return self.__dados

    @dados.setter
    def dados(self, valores):
        self.__dados = self.Cria_Dados(*valores)

    @property
    def permeabilidade(self):
        return self.__permeabilidade

    @permeabilidade.setter
    def permeabilidade(self, *args, **kwargs):
        self.__permeabilidade = 4e-7 * PI

    @property
    def permissividade(self):
        return self.__permissividade

    @permissividade.setter
    def permissividade(self, *args, **kwargs):
        self.__permissividade = 8.854187e-12

    def __Ds(self, raio: float, n_condutores: int, distancia: float, simetrico: bool = True):
        if n_condutores <= 5 and simetrico:
            D = raio * distancia ** (n_condutores - 1)
            if n_condutores == 4:
                x = sqrt(2)
            else:
                x = 1
            D = pow(D * x, 1 / n_condutores)
            return D
        elif not simetrico:
            valores = [raio for i in range(n_condutores)] + self.distancias
            return media_geometrica(*valores)

        else:
            raise NotImplemented("a funcao aida nao foi implementada")

    def get_distancias(self):
        D = {}
        for i in ['AB', 'AC', 'AD', 'AE', 'AF', 'BC', 'BD', 'BE', 'BF', 'CD', 'CE', 'CF']:
            try:
                D[i] = eval("self.dados.DISTANCIA_" + i)
            except Exception as e:
                ...
        return D

    def get_alturas(self):
        H = {}
        for i in "ABCDEF":
            try:
                H[i] = eval("self.dados.ALTURA_" + i) - 0.7 * self.dados.FLECHA
            except Exception as e:
                ...
        return H

    def __get_alturas_para_imagens(self):
        alturas = self.get_alturas()
        distancias_entre_fases = self.get_distancias()
        retorno = {}
        for i, j in distancias_entre_fases.keys():
            retorno[i+j] = (4 * alturas[i] * alturas[j] + distancias_entre_fases[i+j] ** 2) ** .5

        return retorno



    def calculo_indutancia(self):
        distancias_entre_fases = self.get_distancias().values()
        DMG = media_geometrica(*distancias_entre_fases)
        simetria = bool(int(self.dados.CONDUTORES_SIMETRICOS))
        Ds = self.__Ds(self.dados.DIAMETRO_CONDUTOR / 2 * 0.7788,
                       self.dados.NUMERO_CONDUTORES,
                       distancia=self.distancias[0],
                       simetrico=simetria)
        L = self.permeabilidade / 2 / PI * log(DMG / Ds)
        LT = L * self.dados.COMPRIMENTO_LINHA
        XL = 2 * PI * self.dados.FREQUENCIA * L
        XLT = XL * self.dados.COMPRIMENTO_LINHA

        Indutancia = namedtuple("Indutancia", "Indutancia Indutancia_Total Reatancia  Reatancia_Total")
        return Indutancia(L, LT, XL, XLT)

    def calculo_capacitancia(self, efeito_solo=False):
        alturas_para_imagens = self.__get_alturas_para_imagens().values()
        alturas = list(self.get_alturas().values())
        for i, h in enumerate(alturas):
            alturas[i] = 2 * h

        distancia_entre_as_fases = self.get_distancias().values()
        DMG = media_geometrica(*distancia_entre_as_fases)
        simetria = bool(int(self.dados.CONDUTORES_SIMETRICOS))
        Ds = self.__Ds(self.dados.DIAMETRO_CONDUTOR / 2,
                       self.dados.NUMERO_CONDUTORES,
                       distancia=self.distancias[0],
                       simetrico=simetria)

        if efeito_solo:
            k = media_geometrica(*alturas) / media_geometrica(*alturas_para_imagens)
            C = 2 * PI * self.permissividade / log(DMG / Ds * k)

        else:
            C = 2 * PI * self.permissividade / log(DMG / Ds)

        C_total = C * self.dados.COMPRIMENTO_LINHA
        XL = 1 / (2 * PI * self.dados.FREQUENCIA * C)
        XL_total = XL * self.dados.COMPRIMENTO_LINHA
        BC = 1 / C

        Capacitancia = namedtuple("Capacitancia", "Capacitancia Capacitancia_Total Reatancia  Reatancia_Total, Susceptancia_Capacitiva")
        return Capacitancia(C, C_total, XL, XL_total, BC)


if __name__ == "__main__":
    const = ['duplo', 'Segundo', 2323232.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 2,
             10.0, 10.0, 10.0, 10.0, 10.0, 10.0]
    # dis = [10]
    const_simples1 = ['simples', '10', 41.307, 41.156, 41.307, 0.2959, 4, 60.0, 174.03e3, 41.307, 41.156, 41.307, 10.0,
                      0]
    dis_simples = [10, 10, 10]

    const_simples2 = ['simples', '10', 6.096, 6.096, 11.5824, 60, 174.03e3, 24.7534 / 2, 16, 24.7534 / 2, 0, 0.2959, 4,
                      1]

    const_simples = ["simples", "Danilo", 6, 7.5, 6, 60, 300e3, 12, 16, 12, 0, .04, 4, 1]
    const_simples = ["simples", "Danilo", 6.096, 11.5824, 6.096, 60, 300e3, 12, 16, 12, 0, .04, 4, 1]

    dis = [.4 for i in range(4) for j in range(i + 1, 4)]
    dis[-2] = dis[-1] = .4 * sqrt(2)

    c = Calculos(['simples', 'Miracema - Colinas 3', 8.42999, 15.0, 8.42999, 60.0, 174030.0, 41.307, 45.156, 41.307, 0.0, 0.12, 4, '1'], [0.002])
    for i, j in c.calculo_capacitancia(True)._asdict().items():
        print(i, " = ", j)
    exit()
    c = Calculos(const_simples, dis)
    L = c.calculo_indutancia()
    C = c.calculo_capacitancia(True)
    C1 = c.calculo_capacitancia()


    print(C)
    print(C1)
    print(L)
