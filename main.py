#bash /usr/bin/python3

import kivy

kivy.require("1.0.1")
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.properties import ListProperty
from kivy.clock import Clock
from kivy.utils import get_color_from_hex

try:
    from .gera_relatorio import GeraRelatorioWidget
    from .logpopup import LogPopup, PopButton
    from .tela_home import TelaHomeWidget, HomeButton
    from .tela_inserir import TelaInserirWidget
    from .historico import HistoricoWidget
    from .dados import Dados, NOMES_CONSTANTES
    #from .calculos import Calculos
    import unidades
    from .tela_sobre import TelaSobreWidget

except:
    from gera_relatorio import GeraRelatorioWidget
    from logpopup import LogPopup, PopButton
    from tela_home import TelaHomeWidget, HomeButton
    from tela_inserir import TelaInserirWidget
    from historico import HistoricoWidget
    from calculos import Calculos
    from dados import Dados, NOMES_CONSTANTES
    import unidades
    from tela_sobre import TelaSobreWidget

from functools import wraps


class TelaHome(Screen):
    def __init__(self, **kwargs):
        super(TelaHome, self).__init__(**kwargs)
        self.popup = self.constroi_popup()
        self.popup_stat = False

        import time
        t = time.time()
        def f(tempo, *args):
                print(self.key, time.time() - t)

        self.key = 0
        #Clock.schedule_interval(f, 1/30)

    def teclas_atalho(self, win, key, *args):
        if key == 27:
            self.confirmacao_saida()
        return True


    def botoes_enter(self, win, key, *args):

        if key == 13 or key == 271:
            App.get_running_app().stop()
        return True

    def confirmacao_saida(self, *args):
        if self.popup_stat:
            return True

        Window.bind(on_keyboard=self.botoes_enter)

        self.popup.open()
        self.popup_stat = True

        return True


    def on_pre_enter(self, *args):
        Window.bind(on_keyboard=self.teclas_atalho, on_request_close=self.confirmacao_saida)
        return True


    def constroi_popup(self):
        box = BoxLayout(orientation="vertical", padding="10sp", spacing="10sp")
        botoes = BoxLayout(padding="10sp", spacing="10sp")

        def ao_fechar(*args):
            self.popup_stat = False
            Window.unbind(on_keyboard=self.botoes_enter)

        pop = Popup(title="Quer mesmo sair?", content=box, title_size="25sp", size_hint=(.35, .35))
        pop.opacity = .85
        pop.on_dismiss = ao_fechar
        imagem = Image(source="./imagens/atencao.png")

        def botao_sim(*args):
            pop.dismiss()
            self.popuop_stat = False

        sim = PopButton(text="sim", font_size="20sp", on_release=App.get_running_app().stop)
        nao = PopButton(text="nao", font_size="20sp", on_release=botao_sim)
        botoes.add_widget(sim)
        botoes.add_widget(nao)

        box.add_widget(imagem)
        box.add_widget(botoes)
        return pop

class ProjetoApp(App):
    construir_medidas_com_historico = False
    dados = Dados()

    # dados.gera_data_bases()
    icon = "imagens/icone.png"
    kv_file = "projeto.kv"

    def on_start(self):
        pass

    def build(self):
        self.manager = ScreenManager()
        self.constroi_tela_home()

        self.constroi_tela_inserir_constantes("simples")
        self.constroi_tela_inserir_constantes("duplo")
        self.constroi_tela_sobre()

        # self.constroi_tela_historico()

        self.manager.ids["circuito_simples_botao_ok"].bind(on_release=self.button_circuito_botao_ok("simples"))
        self.manager.ids["circuito_duplo_botao_ok"].bind(on_release=self.button_circuito_botao_ok("duplo"))
        # self.manager.current = "circuito_simples"

        return self.manager

    def vai_para_tela(self, nome:str):
        def dentro(*args):
            self.manager.current = nome
        return dentro

    def button_circuito_botao_ok(self, tipo: str):

        def funcao_dentro(*args):
            self.ler_entrada_dados(tipo)
            self.tela_anterior = f"circuito_{tipo}"

        return funcao_dentro

    def button_circuito_duplo_botao_ok(self, button):
        self.ler_entrada_dados("duplo")
        self.tela_anterior = "circuito_duplo"

    def button_circuito_simples_botao_ok(self, button):
        self.ler_entrada_dados("simples")
        self.tela_anterior = "circuito_simples"

    def button_voltar_home(self, button):
        self.manager.current = "home"

    def button_voltar_home_e_apaga_insercoes(self, tipo):
        distancias = [""] * 3
        constantes = [tipo] + [""] * len(NOMES_CONSTANTES[tipo][:-2]) + ["0"]

        def funcao_interna(*argsv):
            self.constroi_telas_a_partir_do_historico(constantes, distancias)
            self.manager.current = "home"

        return funcao_interna

    def button_home_circuito_duplo(self, button):
        self.construir_medidas_com_historico = False
        self.constroi_tela_inserir_constantes("duplo")

    def button_home_circuito_simples(self, button):
        self.construir_medidas_com_historico = False
        self.constroi_tela_inserir_constantes("simples")

    def button_home_historico(self, button):
        self.constroi_tela_historico()

    def button_botoes_historico(self, button):
        key = button.key
        dados = self.dados.ler_do_banco_dados()[key]
        # print(f"Botao {key}, Valor: {dados}")
        constantes, distancias = dados
        self.constroi_telas_a_partir_do_historico(constantes[2:], distancias[1:])

    def button_inserir_distancias_botao_voltar(self, button):
        self.manager.current = self.tela_anterior

    def button_inserir_distancias_botao_ok(self, button):
        self.ler_entrada_distancias()

    def button_home_sair(self, *args, **kwargs):
        # print("chamou")
        tela: TelaHome = self.manager.get_screen("home")

        tela.confirmacao_saida()
        return True


    def button_historico_botao_limpar(self, button):

        # print("limpando banco de dados")
        box = BoxLayout(orientation="vertical", padding="10sp", spacing="10sp")
        botoes = BoxLayout(padding="10sp", spacing="10sp")

        pop = Popup(title="Deseja Limpar o Histórico?", content=box, title_size="25sp", size_hint=(.5, .35))
        pop.opacity = .85
        imagem = Image(source="./imagens/atencao.png")

        def limpa_e_recarrega_hitorico(*args):
            self.dados.gera_data_bases()
            self.constroi_tela_historico()
            pop.dismiss()

        sim = PopButton(text="sim", font_size="20sp", on_release=limpa_e_recarrega_hitorico)
        nao = PopButton(text="nao", font_size="20sp", on_release=pop.dismiss)
        botoes.add_widget(sim)
        botoes.add_widget(nao)

        box.add_widget(imagem)
        box.add_widget(botoes)
        pop.open()

        # self.dados.gera_data_bases()
        # self.constroi_tela_historico()

    def button_relatorio_voltar(self, button):
        self.manager.current = self.tela_anterior

    def constroi_telas_a_partir_do_historico(self, constantes, distancias):
        tipo = constantes[0]
        nome = f"circuito_{tipo}" + "_{}"
        nomes_constantes = NOMES_CONSTANTES[tipo]
        for txt, cons in zip(constantes[1:], nomes_constantes[1:]):
            if cons == "CONDUTORES_SIMETRICOS":
                self.manager.ids[nome.format(cons)].active = int(txt)
                continue
            self.manager.ids[nome.format(cons)].text = str(txt)

        self.manager.current = f"circuito_{tipo}"
        self.construir_medidas_com_historico = True
        self._distancias = distancias

    def constroi_tela_home(self):
        screen = TelaHome(name="home")
        home = TelaHomeWidget(Window.size)
        for chave, valor in home.ids.items():
            self.manager.ids[chave] = valor
        screen.add_widget(home)
        self.manager.add_widget(screen)

        self.manager.ids["home_circuito_simples"].bind(on_release=self.button_home_circuito_simples)
        self.manager.ids["home_circuito_duplo"].bind(on_release=self.button_home_circuito_duplo)
        self.manager.ids["home_historico"].bind(on_release=self.button_home_historico)
        self.manager.ids["home_sobre"].bind(on_release=self.vai_para_tela("sobre"))
        self.manager.ids["home_sair"].bind(on_release=self.button_home_sair)

    def constroi_tela_historico(self):
        nome_tela = "historico"
        if self.manager.has_screen(nome_tela):
            screen = self.manager.get_screen(nome_tela)
            screen.canvas.clear()
        else:
            screen = Screen(name=nome_tela)
            self.manager.add_widget(screen)

        historico = HistoricoWidget(Window.size, self.dados)
        try:
            historico.ids['historico_botao_voltar'].bind(on_release=self.button_voltar_home)
            historico.ids['historico_botao_limpar'].bind(on_release=self.button_historico_botao_limpar)
        except:
            pass
        for chave, valor in historico.ids.items():
            if valor.__class__.__name__.endswith("HistoricoButton"):
                valor.bind(on_press=self.button_botoes_historico)

        screen.add_widget(historico)
        self.manager.current = nome_tela

    def constroi_tela_inserir_constantes(self, tipo):
        assert isinstance(tipo, str)
        nome_tela = f"circuito_{tipo}"
        if self.manager.has_screen(nome_tela):
            self.manager.current = nome_tela
            return

        screen = Screen(name=nome_tela)
        nomes = NOMES_CONSTANTES[tipo]
        tela_inserir = TelaInserirWidget(Window.size, nome_tela, nomes[1:],
                                         titulo=f"Dados para Circuito {tipo}".title())

        screen.add_widget(tela_inserir)
        self.manager.add_widget(screen)

        for chave, valor in tela_inserir.ids.items():
            self.manager.ids[chave] = valor

        self.manager.ids[f"{nome_tela}_botao_voltar"].bind(on_release=self.button_voltar_home)

    def constroi_tela_inserir_medidas(self, numero_condutores):
        nome_tela = "inserir_distancias"

        if self.manager.has_screen(nome_tela):
            screen = self.manager.get_screen(nome_tela)
            screen.canvas.clear()
        else:
            screen = Screen(name=nome_tela)
            self.manager.add_widget(screen)

        simetria = int(self.constantes_lidas[-1])

        if simetria:
            if numero_condutores > 4:
                raise NotImplementedError("Codigo no modulo Calculos nao implementado ... Parando ainda no modulo main")
            nomes_campos = ["Distancia entre os contutores"]
            keys = ["TEXT_INPUT"]
        else:
            nomes_campos = [f"Distancia entre os cabos {i+1} e {j+1}" for i in range(numero_condutores) for j in range(i+1, numero_condutores)]
            keys = [f"TEXT_INPUT{i}" for i, j in enumerate(nomes_campos)]

        inserir = TelaInserirWidget(Window.size, nome_tela, nomes_campos, "Entre com as distancias".title(), keys=keys)
        screen.add_widget(inserir)

        n = 0
        for chave, valor in inserir.ids.items():
            if self.construir_medidas_com_historico and "TEXT_INPUT" in chave:
                try:
                    valor.text = str(self._distancias[n])
                except:
                    valor.text = ""
                n += 1

            self.manager.ids[chave] = valor

        self.manager.ids[f"{nome_tela}_botao_voltar"].bind(on_release=self.button_inserir_distancias_botao_voltar)
        self.manager.ids[f"{nome_tela}_botao_ok"].bind(on_release=self.button_inserir_distancias_botao_ok)

        # self.manager.current = nome_tela

    def constroi_tela_sobre(self):
        nome_tela = "sobre"
        screen = Screen(name=nome_tela)
        dados = [
            ["Programa desenvolvido pelos estudantes",],
            ["Danilo C Nascimento", "danilo.nascimento@uft.edu.br"],
            ["Danilo C Nascimento", "danilo.nascimento@uft.edu.br"],
            ["Danilo C Nascimento", "danilo.nascimento@uft.edu.br"],
            ["Danilo C Nascimento", "danilo.nascimento@uft.edu.br"],
            ["Danilo C Nascimento", "danilo.nascimento@uft.edu.br"],
            ["Kayo Nascimento", "email.kayo@mail.com"],
            ["Shamella Castro", "email.shamella@mail.com"]
        ]
        tela = TelaSobreWidget(titulo="Sobre os Desenvolvedores", dados=dados)
        tela.ids["sobre_botao_voltar"].bind(on_release=self.vai_para_tela("home"))
        screen.add_widget(tela)
        self.manager.add_widget(screen)

    def constroi_tela_gera_relatorio(self):
        # print("Aqui serão gerados os relatórios")

        nomes = self.dados.get_valores_de_um_campo("NOME")

        if self.NOME not in nomes:
            self.dados.salva_no_banco_dados([self.constantes_lidas_para_salvar, self.distancias_lidas_para_salvar])

        nome_tela = "gera_relatorio"
        if self.manager.has_screen(nome_tela):
            screen = self.manager.get_screen(nome_tela)
            screen.canvas.clear()
        else:
            screen = Screen(name=nome_tela)
            self.manager.add_widget(screen)

        #Execura os calculos
        calculos = Calculos(self.constantes_lidas, self.distancias_lidas)
        indutancia = calculos.calculo_indutancia()
        capacitancia = calculos.calculo_capacitancia(True)

        lista_tratada = []
        unidade = "H/m H Ω/m Ω F/m F Ω/m Ω S".split()
        num = unidades.para_notacao_cientifica(indutancia[1], unidade[1], 4)
        for i, numero in enumerate(list(indutancia) + list(capacitancia)):
            try:
                num = unidades.para_notacao_cientifica(numero, unidade[i], 4)
                num = str(num).replace(".", ",")
                lista_tratada.append(num)
            except Exception as e:
                lista_tratada.append(numero)
                print("Erro", e)

        descricao = "Indutancia,Indutancia_Total,Reatancia_Indutiva,Reatancia Indutiva Total".split(",")
        descricao += "Capacitancia,Capacitancia Total,Reatancia Capacitiva,Reatancia Capacitiva Total, Susceptancia Capacitiva".split(",")
        dic = [(f"Descrição {i}", f"Valor {i}") for i in range(1, 20)]

        valores = list(zip(descricao, lista_tratada))


        #print(valores)
        dic = dict(valores)
        for i in range(1, 4):
            txt = " " * i
            dic[txt] = ""

        relatorio = GeraRelatorioWidget(Window.size, nome_tela, "Relatórios", dic)
        relatorio.ids[f"{nome_tela}_botao_voltar"].bind(on_release=self.button_relatorio_voltar)

        tipo = self.constantes_lidas[0]

        relatorio.ids[f"{nome_tela}_botao_home"].bind(on_release=self.button_voltar_home_e_apaga_insercoes(tipo))

        screen.add_widget(relatorio)
        self.manager.current = nome_tela

    def ler_entrada_dados(self, tipo: str):
        """
        :param tipo: str ["simples", "duplo", "medidas"]
        :param constantes: list
        :return: list
        """
        numero_condutores = 0

        if tipo == "simples":
            constantes = NOMES_CONSTANTES["simples"]
        elif tipo == "duplo":
            constantes = NOMES_CONSTANTES["duplo"]
        else:
            texto = f"tipo nao percence a " + ", \"{}\"" * 3
            raise ValueError(texto.format("simples", "duplo"))

        constantes_lidas = []
        self.constantes_lidas_para_salvar = [tipo]

        logs = []
        texto_log = "O campo [b]{}[/b] {}"

        simetria = False

        nome_tela = "obtem_medidas"
        if tipo != "medidas":
            constantes_lidas = [tipo]  # [f"\"{tipo}\""]
            nome_tela = f"circuito_{tipo}"

        for nome in constantes[1:]:
            id = f"{nome_tela}_{nome}"
            texto_label = " ".join(nome.split("_"))

            if nome == "CONDUTORES_SIMETRICOS":
                if self.manager.ids[id].active:
                    lido = "1"
                    simetria = True
                else:
                    lido = "0"
                    simetria = False
                constantes_lidas.append(lido)
                self.constantes_lidas_para_salvar.append(lido)
                continue
            lido = str(self.manager.ids[id].text)
            self.constantes_lidas_para_salvar.append(lido)
            lido = lido.replace(",", ".")

            try:
                lido = unidades.de_notacao_cientifica(lido)
                lido = str(lido)
            except:
                pass

            if lido == "":
                logs.append(texto_log.format(texto_label, "está vazio"))
            elif nome == "NUMERO_CONDUTORES":
                try:
                    lido = int(lido)
                    numero_condutores = lido
                    if lido <= 0:
                        logs.append(texto_log.format(texto_label, "deve ser maior que 0"))
                    if lido > 15:
                        logs.append(texto_log.format(texto_label, "deve ser menor ou igual a 15"))
                except:
                    logs.append(texto_log.format(texto_label, "não é inteiro"))


            elif nome != "NOME":

                try:
                    lido = float(lido)
                except:
                    logs.append(texto_log.format(texto_label, "não é real"))

            constantes_lidas.append(lido)

        self.NOME = constantes_lidas[1]

        if simetria and numero_condutores > 4:
            logs.append("Ainda não há implementação para calculos com mais de 4 consdutores simétricos")


        if logs:
            popup = LogPopup(Window.size, logs, opacity=.75)
            popup.open()
        elif numero_condutores > 1:
            self.constantes_lidas = constantes_lidas
            self.constroi_tela_inserir_medidas(numero_condutores)
            self.numero_condutores = numero_condutores
            self.manager.current = "inserir_distancias"

        elif numero_condutores == 1:
            self.distancias_lidas = []
            self.constantes_lidas = constantes_lidas
            self.constroi_tela_gera_relatorio()

    def ler_entrada_distancias(self):
        nome_tela = "inserir_distancias"

        simetria = int(self.constantes_lidas[-1])

        if simetria:
            if self.numero_condutores > 4:
                raise NotImplementedError("Codigo no modulo Calculos nao implementado ... Parando ainda no modulo main")
            nomes_campos = ["Distancia entre os contutores"]
            keys = ["TEXT_INPUT"]

        else:
            nomes_campos = [f"Distancia entre os cabos {i + 1} e {j + 1}" for i in range(self.numero_condutores) for j in range(i + 1, self.numero_condutores)]
            keys = [f"TEXT_INPUT{i}" for i, j in enumerate(nomes_campos)]

        distancias_lidas = []
        self.distancias_lidas_para_salvar = []


        logs = []
        texto_log = "O campo [b]{}[/b] {}"
        for nome, campo in zip(keys, nomes_campos):
            lido = str(self.manager.ids[f"{nome_tela}_{nome}"].text)
            self.distancias_lidas_para_salvar.append(lido)
            lido = lido.replace(",", ".")

            try:
                lido = unidades.de_notacao_cientifica(lido)
                lido = str(lido)
            except:
                ...

            if lido == "":
                logs.append(texto_log.format(campo, "está vazio"))
            else:
                try:
                    lido = float(lido)
                except:
                    logs.append(texto_log.format(campo, "nao é real"))

            distancias_lidas.append(lido)
        # print(distancias_lidas)
        self.distancias_lidas = distancias_lidas

        if logs:
            popup = LogPopup(Window.size, logs, opacity=.75)
            popup.open()
        else:
            self.distancias_lidas = distancias_lidas
            self.constroi_tela_gera_relatorio()


if __name__ == "__main__":
    from kivy.config import Config
    from kivy.core.text import LabelBase

    # print("meio", get_color_from_hex("6b7c85"))
    # print("laranja", get_color_from_hex("fCB001"))

    LabelBase.register(name="Roboto",
                       fn_regular="./fontes/Roboto-Thin.ttf",
                       fn_bold="./fontes/Roboto-Medium.ttf")

    altura = 650
    largura = 800

    Config.set("graphics", "width", largura)
    Config.set("graphics", "height", altura)
    Config.set("input", "mouse", "mouse,disable_multitouch")
    Config.set("graphics", "resizable", False)

    from kivy.core.window import Window

    Window.size = (largura, altura)

    Window.clearcolor = get_color_from_hex("4C6B8A")
    Window.clearcolor = get_color_from_hex("1ABC9C")
    Window.clearcolor = get_color_from_hex("#22A178")
    Window.clearcolor = get_color_from_hex("#040348")

    print(altura, largura)

    ProjetoApp().run()
