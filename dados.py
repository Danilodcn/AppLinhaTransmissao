import sqlite3
import os

CONSTANTES_SIMPLES = ['TIPO',
                      'NOME',
                      'DISTANCIA_AB',
                      'DISTANCIA_AC',
                      'DISTANCIA_BC',
                      'FREQUENCIA',
                      'COMPRIMENTO_LINHA',
                      'ALTURA_A',
                      'ALTURA_B',
                      'ALTURA_C',
                      'FLECHA',
                      'DIAMETRO_CONDUTOR',
                      'NUMERO_CONDUTORES',
                      "CONDUTORES_SIMETRICOS"]

CONSTANTES_DUPLO = ['TIPO',
                    'NOME',
                    'DISTANCIA_AB',
                    'DISTANCIA_AC',
                    'DISTANCIA_AD',
                    'DISTANCIA_AE',
                    'DISTANCIA_AF',
                    'DISTANCIA_BC',
                    'DISTANCIA_BD',
                    'DISTANCIA_BE',
                    'DISTANCIA_BF',
                    'DISTANCIA_CD',
                    'DISTANCIA_CE',
                    'DISTANCIA_CF',
                    'FREQUENCIA',
                    'COMPRIMENTO_LINHA',
                    'ALTURA_A',
                    'ALTURA_B',
                    'ALTURA_C',
                    'ALTURA_D',
                    'ALTURA_E',
                    'ALTURA_F',
                    'FLECHA',
                    'DIAMETRO_CONDUTOR',
                    'NUMERO_CONDUTORES',
                    "CONDUTORES_SIMETRICOS"]

NOMES_CONSTANTES = {"simples": CONSTANTES_SIMPLES, "duplo": CONSTANTES_DUPLO}


class Dados:
    def __init__(self, db="banco_dados.db", constantes_nomes=None):
        self.db = db

        if constantes_nomes is None:
            self.constantes = CONSTANTES_DUPLO
        else:
            self.constantes = constantes_nomes

        if not os.path.isfile(self.db):
            self.gera_data_bases()


    def gera_data_bases(self):
        if os.path.isfile(self.db):
            # print("apagando ", i)
            os.remove(self.db)
            pass
        con = sqlite3.connect(self.db)
        # cur = con.cursor()
        # cur.execute("create table teste (teste real);")

        add = ""
        for item in self.constantes:
            tipo = "real"
            if item == 'NUMERO_CONDUTORES':
                tipo = "text"#"integer"

            elif item == "NOME":
                tipo = "text"

            elif item == "TIPO":
                tipo = f"text NOT NULL CHECK ({item} IN (\"simples\", \"duplo\"))"

            elif item == "CONDUTORES_SIMETRICOS":
                tipo="bit"

            add += f", {item} {tipo}"

        sql = "create table CONSTANTES (ID integer primary key autoincrement, DATA date" + add + ");"
        #print(sql)
        # print(sql, "Cricacao da tabela")
        con.execute(sql)
        con.execute(f"create table DISTANCIAS (ID integer, " + ", ".join([f"A{i}" for i in range(200)]) + ");")
        # con.execute("insert into CONSTANTES (TIPO, DATA) values (\'simples\', datetime(\"now\", \"localtime\"))")
        # con.commit()

        # cur.execute("select datetime(\"now\", \"localtime\")")
        # cur.execute("select * from CONSTANTES")
        con.close()

    def ler_dados(self):
        print(f"LEITURA DE DADOS PARA A TABELA CONSTANTES")
        dados_constantes = []
        numero_condutores = 0
        for i, valor in enumerate(self.constantes):
            texto = f"insira o valor da constante {valor}: "
            lido = input(texto)
            if valor == "NUMERO_CONDUTORES":
                lido = np.int(lido)
                numero_condutores = lido
            else:
                lido = np.float(lido)

            dados_constantes.append(lido)
        dados_distancias = []
        if numero_condutores > 1:
            for i in range(numero_condutores - 1):
                x = input(f"Entre com a distancia do cabo 1 ao cabo {i}: ")
                dados_distancias.append(float(x))

        return dados_constantes, dados_distancias

    def ler_do_banco_dados(self):
        retorno:dict = {}

        sql = "select * from CONSTANTES"
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        cur.execute(sql)
        dados_constantes = cur.fetchall()
        cur.execute("select ID from CONSTANTES")
        keys = cur.fetchall()
        #print(dados)
        # dados_distancias = []

        cur.execute(f"select * from DISTANCIAS")
        dados_distancias = cur.fetchall()
        for key in keys:
            key = key[0]
            dados_lidos = [i for i in dados_constantes[key - 1] if i != None]

            dis = [i for i in dados_distancias[key - 1] if i != None]

            retorno[f"{key}"] = [dados_lidos, dis]


        return retorno

    def salva_no_banco_dados(self, tabelas):
        """
        :type tabelas: list
        """
        # print(tabelas)
        constantes, distancias = tabelas
        # print(distancias)
        #print("0, ", constantes, distancias, tabelas)
        tipo, constantes = constantes[0], constantes[1:]

        if tipo == "simples":
            nomes = CONSTANTES_SIMPLES

        elif tipo == "duplo":
            nomes = CONSTANTES_DUPLO

        else:
            raise ValueError("Erro, o valor passado na variável <tipo> não é valido: {}".format(tipo))

        #nome = constantes[0]
        #nome = f"\"{nome}\""
        #constantes[0] = nome
        for i, valor in enumerate(constantes):
            constantes[i] = f'"{valor}"'

        for i, valor in enumerate(distancias):
            distancias[i] = f'"{valor}"'

        sql = f"insert into CONSTANTES (DATA, " + ", ".join(
            nomes) + f") values (datetime(\'now\',\'localtime\'), \'{tipo}\', " + ", ".join(
            list(map(str, constantes))) + ");"
        # input(sql)
        print(sql)
        con = sqlite3.connect(self.db)
        con.execute(sql)
        numero_condutores = len(distancias) + 1

        key = self.ultimo_key()
        distancias = [key+1] + distancias

        if numero_condutores > 1:
            nomes = [f"A{i}" for i in range(numero_condutores - 1)]
            id = "ID, "
        else:
            nomes = []
            id = "ID"
        sql = f"insert into DISTANCIAS ({id}" + ", ".join(nomes) + ") values (" + ", ".join(list(map(str, distancias))) + ");"
        con.execute(sql)

        con.commit()
        con.close()

    def get_valores_de_um_campo(self, *campos):
        texto = ", ".join(campos)
        sql = f"select {texto} from CONSTANTES"
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        cur.execute(sql)
        retorno = cur.fetchall()
        if len(campos) == 1:
            retorno = [dado[0] for dado in retorno]
        # input(retorno)
        return retorno

    def ultimo_key(self):

        sql = "select ID from CONSTANTES"
        con = sqlite3.connect(self.db)
        cur = con.cursor()
        cur.execute(sql)
        dados = cur.fetchall()
        con.close()
        # print(dados)
        if not dados:
            return 0
        return dados[-1][0]


if __name__ == "__main__":
    dados = Dados()
    #dados.ler_dados()
    dados.gera_data_bases()
    #dados.salva_no_banco_dados([["simples", "opa"] + [i for i in range(11)], [3.3] * 3])
    # dados.salva_no_banco_dados([["simples", "Segundo"] + [i for i in range(11)], [4.654, 8998.988, 99.22]])
    #dados.salva_no_banco_dados(
        #[["duplo", "Segundo"] + [i for i in range(len(CONSTANTES_DUPLO) - 2)], [4.654, 8998.988, 99.22]])

    dados.salva_no_banco_dados([["simples", "Esse e o teste"] + [i for i in range(11)], []])

    x = dados.ler_do_banco_dados()
    print(x)
    """for i in range(10):
        dados.salva_no_banco_dados([["opa"] + [i for i in range(11)], [3.3] * 3])
        pass
    x = dados.ler_do_banco_dados()
    print(x)
    for i, value in x.items():
        print(i, value)"""
