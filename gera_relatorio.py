from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.actionbar import ActionBar, ActionView, ActionPrevious, ActionButton, ActionLabel, ActionSeparator
from kivy.graphics import Color, Rectangle
from kivy.utils import get_color_from_hex
from kivy.metrics import sp



class OkButton(Button):
    pass

class VoltarButton(Button):
    pass

class SetaButton(Button):
    pass

class GeraRelatorioWidget(GridLayout):
    n = 0
    cols = 1

    def __init__(self, size, nome_tela, titulo="Titulo Padrão", dicionario: dict={}, **kwargs):
        super(GeraRelatorioWidget, self).__init__(**kwargs)
        self.size = size
        self.titulo = titulo
        self.nome_tela = nome_tela
        self.fonte_padrao = sp(20)
        self.dicionario = dicionario

        self.constroi_titulo()
        #self.add_widget(self.constroi_linha_relatorio("des", "valor"))
        self.constroi_relatorio()
        self.add_widget(Label(size_hint_y=None, height=self.height*.05))

    def constroi_linha_relatorio(self, descricao: str, valor: str):
        valor = str(valor)
        self.n += 1
        n = 1
        grid = GridLayout(cols=2)
        label = Label(text=descricao)
        label.size_hint_y = None
        label.height = self.height * .2
        label.font_size = self.fonte_padrao * n
        label.valign = "center"
        label.halign = "center"
        label.text_size = [self.width*.45, self.height*.9]

        grid.add_widget(label)
        #grid.ids["descricao"] = label

        label = Label(text=valor)
        label.size_hint_y = None
        label.halign = label.valign = "center"
        label.text = valor
        label.height = self.height * .2
        label.font_size = self.fonte_padrao * n
        label.text_size = [self.width * .45, self.height * .9]

        grid.add_widget(label)
        #grid.ids["valor"] = label

        #self.ids[f"{self.nome_tela}_campo_{self.n}"] = grid
        return grid

    def constroi_relatorio(self):
        #print("Dicionario", self.dicionario)
        if self.dicionario == {}:
            grid = GridLayout(cols=1)
            grid.add_widget(Label(text="Sem dados para mostrar no relatorio", font_size=self.fonte_padrao))
            self.add_widget(grid)
            return

        spacing = "60sp"
        padding = [f"{i}sp" for i in [10, 0, 10, 50]]

        grid = GridLayout(cols=1, size_hint_y=None, spacing=spacing, padding=padding)
        grid.bind(minimum_height=grid.setter("height"))


        for descricao, valor in self.dicionario.items():
            linha = self.constroi_linha_relatorio(descricao, valor)
            grid.add_widget(linha)

        scroll = ScrollView(size_hint_y=.75)
        scroll.height = self.height * .85
        scroll.add_widget(grid)

        self.add_widget(scroll)


    def constroi_titulo(self):
        font_size = self.fonte_padrao
        bar = ActionBar()
        view = ActionView()
        btn_voltar = ActionPrevious(app_icon="./imagens/icone.png")
        btn_voltar.title = self.titulo.title()
        btn_voltar.size_hint = .7, .7

        view.add_widget(btn_voltar)
        titulo = btn_voltar.ids["title"]
        titulo.font_name = "Roboto"
        titulo.color = [0.9882352941176471, 0.6901960784313725, 0.00392156862745098, 1]
        titulo.font_size = font_size * 1.3

        btn_home = ActionButton(text="Home", font_size=font_size)

        view.add_widget(btn_home)
        with view.canvas:
            Color(*get_color_from_hex("#040348"))
            Rectangle(size=(self.width * 2, self.height * 2))
        bar.add_widget(view)

        self.add_widget(bar)
        self.ids[f"{self.nome_tela}_botao_home"] = btn_home
        self.ids[f"{self.nome_tela}_botao_voltar"] = btn_voltar
