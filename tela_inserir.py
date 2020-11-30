from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.checkbox import CheckBox
from kivy.uix.spinner import Spinner
from kivy.uix.actionbar import ActionBar, ActionView, ActionPrevious, ActionButton, ActionLabel, ActionSeparator
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty

from kivy.utils import get_color_from_hex
from kivy.metrics import sp

from string import ascii_letters

class OkButton(Button):
    pass

class VoltarButton(Button):
    pass

class TituloAction(ActionView):
    pass



class TelaInserirWidget(GridLayout):

    def __init__(self, size, nome_tela, lista, titulo="Titulo Padrão", keys=[], **kwargs):
        super(TelaInserirWidget, self).__init__(**kwargs)
        self.size = size
        self.nome_tela = nome_tela
        self.titulo = titulo
        self.lista = lista
        self.keys = keys if keys else lista

        self.fonte_padrao = sp(18)

        b = Label()

        def f(s, t):
            b.text = t
            print(s, t)

        self.constroi_titulo()

        self.insere_scroll_view(lista)

        #label = Label(text="FIM", size_hint=(1, None), height=self.height*.05)



    def insere_scroll_view(self, lista):
        """

        :type lista: list, tuple
        """
        x, y = self.width / 300, self.height / 650
        padding = (10 * x, 10 * y, 10 * x, 10 * y)
        padding = [f"{i}sp" for i in [50, 20, 50, 50]]
        spacing = "20sp"
        grid = GridLayout(cols=2, padding=padding, spacing=spacing, size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))

        for i, nome in enumerate(lista):
            texto = str.split(nome, "_")
            label = Label(text=" ".join(texto), size_hint_y=None, height=self.height*.05, font_size=self.fonte_padrao)
            label.text_size = self.width * .45, label.height * .9
            label.valign = label.halign = "center"

            if nome == "CONDUTORES_SIMETRICOS":
                check = CheckBox(active=0)
                check.size_hint = (2, 2)
                grid.add_widget(label)
                grid.add_widget(check)
                self.ids[f"{self.nome_tela}_{self.keys[i]}"] = check
                continue

            inp = TextInput(size_hint_y=None, height=self.height*.06, border=[4] * 4, font_size=self.fonte_padrao)
            filtro = "float"
            if nome == "NOME":
                filtro = None
            elif nome == "NUMERO_CONDUTORES":
                filtro = "int"

            #inp.input_filter = filtro
            inp.write_tab = False

            grid.add_widget(label)
            grid.add_widget(inp)

            self.ids[f"{self.nome_tela}_{self.keys[i]}"] = inp


        scroll = ScrollView(size_hint_y=.65)
        scroll.width = self.width * .9
        scroll.height = self.height * .85
        scroll.add_widget(grid)
        self.add_widget(scroll)


    def constroi_titulo(self):
        font_size = self.fonte_padrao
        bar = ActionBar()
        view = ActionView()
        btn_voltar = ActionPrevious(app_icon="./imagens/icone.png")
        btn_voltar.title = self.titulo.title()
        btn_voltar.size_hint = .8, .8

        view.add_widget(btn_voltar)
        titulo = btn_voltar.ids["title"]
        titulo.font_name = "Roboto"
        titulo.color = [0.9882352941176471, 0.6901960784313725, 0.00392156862745098, 1]
        titulo.font_size = font_size * 1.3

        btn_ok = ActionButton(text="OK", font_size=font_size)

        view.add_widget(btn_ok)
        bar.add_widget(view)

        with view.canvas:
            Color(*get_color_from_hex("#040348"))
            Rectangle(size=(self.width * 3, self.height * 3))

        self.add_widget(bar)
        self.ids[f"{self.nome_tela}_botao_ok"] = btn_ok
        self.ids[f"{self.nome_tela}_botao_voltar"] = btn_voltar

    def constroi_titulo2(self):
        x, y = self.width / 300, self.height / 650

        padding = (5 * x, 0 * y, 10 * x, 10 * y)
        grid = GridLayout(cols=3, padding=(5, 0, 5, 0), spacing=x * 10)
        grid.size_hint_y = None
        grid.height = self.height * .1

        btn_ok = OkButton(size_hint_x=None, width=self.width*.1)
        btn_voltar = VoltarButton(size_hint_x=None, width=self.width*.1)
        label = Label(text=self.titulo)
        label.font_size = self.fonte_padrao

        grid.add_widget(btn_voltar)
        grid.add_widget(label)
        grid.add_widget(btn_ok)
        self.add_widget(grid)

        self.ids[f"{self.nome_tela}_botao_ok"] = btn_ok
        self.ids[f"{self.nome_tela}_botao_voltar"] = btn_voltar
