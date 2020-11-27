from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.checkbox import CheckBox
from kivy.core.window import Window
from kivy.clock import Clock


class HomeButton(Button):
    pass

class TelaHomeWidget(GridLayout):

    titulo = "Calculo dos Parâmetros da Linha de Transmissão"

    descricao = "Este programa foi uma continuidade do trabalho do Kayo Nascimento \n\n" \
                "[size=23sp]Desenvolvedores: \nDanilo Nascimento\nKayo Nascimento\nShâmella Castro[/size]"

    def __init__(self, size, **kwargs):
        #assert isinstance(size, tuple)
        super(TelaHomeWidget, self).__init__(**kwargs)
        self.size = size

        self.fonte_padrao = "25sp"

        self.constroi_titulo()
        self.constroi_descricao()
        bnt1 = self.constroi_botao("Circuito Simples")
        bnt2 = self.constroi_botao("Circuito Duplo")
        bnt3 = self.constroi_botao("Histórico", "Historico")
        bnt4 = self.constroi_botao("Sobre")
        bnt5 = self.constroi_botao("Sair")

        padding = [f"{i}sp" for i in [150, 15, 150, 15]]
        spacing = "10sp"
        grid = GridLayout(cols=1, padding=padding, spacing=spacing, height=self.height/3)

        grid.add_widget(bnt1)
        grid.add_widget(bnt2)
        grid.add_widget(bnt3)
        grid.add_widget(bnt4)
        grid.add_widget(bnt5)
        self.add_widget(grid)

        check = CheckBox(active=1)

        #grid.add_widget(check)



    def constroi_titulo(self):
        label = Label(text=self.titulo, bold=True)
        label.size_hint_y = None
        label.height = self.size[1] * .1
        label.font_size = self.fonte_padrao
        label.font_size *= 1.3
        self.add_widget(label)

    def constroi_descricao(self):
        grid = GridLayout(cols=2, padding='10sp', spacing="20sp", size_hint_y = 2)
        label = Label(text=self.descricao)
        #label.size_hint_y = None
        label.height = self.size[1] * .6
        label.font_size = self.fonte_padrao
        label.text_size = (self.width * .4, label.height * 1)
        label.valign = "center"
        label.halign = "center"
        imagem = Image(source="./imagens/torre.jpg")

        grid.add_widget(label)
        grid.add_widget(imagem)
        self.add_widget(grid)

    def constroi_botao(self, texto, nome_botao=""):
        """
        :type texto: str
        """
        if nome_botao == "": nome_botao = texto

        bnt = HomeButton(text=texto)
        bnt.font_size = self.fonte_padrao
        #bnt.size_hint_y = None
        #bnt.height = self.height * .1
        texto = texto.split()
        texto = "_".join(texto).lower()
        nome_botao = nome_botao.split()
        nome_botao = "_".join(nome_botao).lower()
        self.ids[f"home_{nome_botao}"] = bnt
        return bnt
