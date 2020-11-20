from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.metrics import sp
from kivy.uix.actionbar import ActionBar, ActionView, ActionPrevious, ActionButton, ActionLabel, ActionSeparator
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Rectangle


try:
    from .dados import Dados
    from .logpopup import PopButton
except:
    from dados import Dados
    from logpopup import PopButton

from datetime import datetime
from time import strftime


def processa(string: str):
    data, hora = string.split()
    retorno = data.split("-") + hora.split(":")

    return [int(i) for i in retorno]

meses = {'1': 'janeiro',
         '2': 'fevereiro',
         '3': 'março',
         '4': 'abril',
         '5': 'maio',
         '6': 'junho',
         '7': 'julho',
         '8': 'agosto',
         '9': 'setembro',
         '10': 'outubro',
         '11': 'novembro',
         '12': 'dezembro'}

def trata_data(string: str):
    atual = strftime("%Y-%m-%d %H:%M:%S")

    atual = datetime(*processa(atual))

    data_salva = processa(string)
    salvo = datetime(*data_salva)

    dt = atual - salvo

    dt_dias = atual.date() - salvo.date()

    hora = datetime(*data_salva).time()
    hora = "as {}".format(hora)
    dia = datetime(*data_salva).date()
    dia = str(dia)
    if dt_dias.days < 2:
        if dt_dias.days == 0:
            dia = "Hoje"
        else:
            dia = "Ontem"

        if dt.seconds < 60 * 60 and dt.days == 0:
            m, s = divmod(dt.seconds, 60)
            if m > 0:
                hora = "a {} minuto".format(m)
                if m > 1:
                    hora += "s"

                if s >= 1:
                    hora += " e {} segundo".format(s)
                    if s > 1:
                        hora += "s"

            else:
                if s >= 1:
                    hora = "a {} segundo".format(s)
                    if s > 1:
                        hora += "s"
    #print(dia.split("-"))
    try:
        a, m, d = dia.split("-")
        m = str(int(m))
        d = int(d)
        dia = f"{d} de {meses[m]} de {a}"
    except:
        pass

    txt = dia + " " + hora

    return txt

#x = trata_data("2020-06-06 19:27:24")
#print(x)

class HistoricoButton(Button):
    def __init__(self, key, **kw):
        super(HistoricoButton, self).__init__(**kw)
        self.key = key

    pass


class LimpaDadosButton(Button):
    pass


class HistoricoLabel(Label):
    pass


class VoltarButton(Button):
    pass


class HistoricoWidget(GridLayout):
    cols = 1

    def __init__(self, size, dados: Dados, **kw):
        """
        :type dados: Dados
        """
        super(HistoricoWidget, self).__init__(**kw)
        self.size = size
        self.dados = dados
        self.fonte_padrao = sp(25)
        self.titulo = "Histórico"
        # self.add_widget(Button(text="ola"))

        self.constroi_titulo()
        self.insere_scroll_view()
        # x = self.constroi_linha_historico(1, "10-02-1997 10:20:59", "Aquela grande descreiçao dosoais sioaiso isoasio, entai m,oskm skjskj s s" , "Simples")
        # self.add_widget(x)

    # x = self.constroi_linha_historico(2, "10-02-1997 10:20:59", "Segundo", "Duplo")
    # self.add_widget(x)

    # print(self.ids)

    def constroi_titulo(self):
        font_size = self.fonte_padrao
        bar = ActionBar()
        view = ActionView()
        btn_voltar = ActionPrevious(app_icon="./imagens/icone.png")
        btn_voltar.size_hint = (.7, .7)
        btn_voltar.title = self.titulo.title()

        view.add_widget(btn_voltar)
        titulo = btn_voltar.ids["title"]
        titulo.font_name = "Roboto"
        titulo.color = [0.9882352941176471, 0.6901960784313725, 0.00392156862745098, 1]
        titulo.font_size = font_size * 1.3

        btn_limpar = ActionButton(text="Limpar", font_size=font_size)
        #btn_limpar.on_release = self.button_limpa_db
        #print(btn_limpar.ids)

        with view.canvas:
            Color(*get_color_from_hex("#040348"))
            Rectangle(size=self.size)

        view.add_widget(btn_limpar)
        bar.add_widget(view)

        self.add_widget(bar)
        self.ids[f"historico_botao_limpar"] = btn_limpar
        self.ids[f"historico_botao_voltar"] = btn_voltar

    def constroi_titulo2(self):
        x, y = self.width / 300, self.height / 650

        padding = (5 * x, 0 * y, 10 * x, 10 * y)
        grid = GridLayout(cols=3, padding=(5, 0, 5, 0), spacing=x * 10)
        grid.size_hint_y = None
        grid.height = self.height * .1

        branco = LimpaDadosButton(size_hint_x=None, width=self.width * .1, on_press=self.button_fecha)
        btn_voltar = VoltarButton(size_hint_x=None, width=self.width * .1)
        label = Label(text=self.titulo, bold=True)
        label.font_size = self.fonte_padrao * 1.5

        grid.add_widget(btn_voltar)
        grid.add_widget(label)
        grid.add_widget(branco)
        self.add_widget(grid)

        self.ids[f"historico_botao_voltar"] = btn_voltar
        self.ids["historico_botao_fechar"] = btn_voltar


    def constroi_linha_historico(self, id, data, nome, tipo):
        id = str(id)
        #print(data)
        data = trata_data(data)
        padding = (self.width * .1, 0, self.width * .1, 0)
        root = GridLayout(rows=1, size_hint_y=None, height=self.height * .15)
        labels = GridLayout(cols=1, padding=padding)
        label_nome = Label(text=f"Nome: [b]{nome}[/b]", font_size=self.fonte_padrao * 1.1, bold=False,
                           text_size=(self.width * .8, root.height / 2), halign="center", valign='center', markup=True)
        label_tipo = Label(text="Circuito [b]{}[/b]".format(tipo.title()), font_size=self.fonte_padrao*.8, bold=False, markup=True)
        label_data = Label(text=f"{data}", font_size=self.fonte_padrao*.8, bold=False)

        labels.add_widget(label_nome)
        tipo_data = GridLayout(cols=1)
        tipo_data.add_widget(label_tipo)
        tipo_data.add_widget(label_data)
        labels.add_widget(tipo_data)
        root.add_widget(labels)
        button = HistoricoButton(id, size_hint_x=None, width=self.width * .1)
        padding = (0, root.height / 5, 0, root.height / 5)
        gri_butao = GridLayout(cols=1, padding=padding, size_hint_x=None, width=self.width * .1)
        gri_butao.add_widget(button)
        root.add_widget(gri_butao)

        self.ids[f"historico_{id}"] = button
        return root

    def insere_scroll_view(self):
        dic_lido = self.dados.ler_do_banco_dados()
        # print(dic_lido)
        if dic_lido == {}:
            label = Label(text="A base da dados está vazia", font_size=self.fonte_padrao * 1.2)
            self.add_widget(label)
            return
        spacing = "20sp"
        root = GridLayout(cols=1, size_hint_y=None, spacing=spacing)
        root.bind(minimum_height=root.setter("height"))

        for key, tabelas in dic_lido.items():
            constantes, _ = tabelas
            id, data, tipo, nome = constantes[:4]
            linha = self.constroi_linha_historico(id, data, nome, tipo)

            root.add_widget(linha)

        scroll = ScrollView(size_hint_y=None)
        scroll.height = self.height * .85
        scroll.add_widget(root)

        self.add_widget(scroll)
