from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.metrics import sp
from kivy.utils import get_color_from_hex

class PopButton(Button):
    pass


class LogPopup(Popup):

    def __init__(self, size, logs=[], **kwargs):
        """
        :type logs list
        """

        super(LogPopup, self).__init__(**kwargs)
        self.size = size
        self.logs = logs
        self.title = "Erros Foram Encontrados"
        self.title_align = "center"
        self.opacity = .85
        self.background_color = get_color_from_hex("#008080")

        self.size_hint_x = .95
        self.size_hint_y = .8

        self.fonte_padrao = sp(20)

        self.title_size = sp(25)


        box = GridLayout(cols=1)

        scroll = self.constroi_mensagem()
        box.add_widget(scroll)

        botao = PopButton(text="Sair", font_name="Roboto", font_size=self.fonte_padrao, size_hint_y=.15, on_release=self.dismiss)
        box.add_widget(botao)

        self.content = box


    def constroi_mensagem(self):
        grid = GridLayout(cols=1, size_hint_y=None)
        grid.bind(minimum_height=grid.setter("height"))


        for log in self.logs:
            #print("criando: ", log)
            log = "[color=008080]" + log + "[/color]"
            label = Label(text=log)
            label.size_hint_y = None
            label.height = self.height*.1
            label.markup = True
            label.font_size = self.fonte_padrao
            label.text_size = self.width * .9, self.height * 1
            label.halign = label.valign = "center"

            grid.add_widget(label)

        scroll = ScrollView(size_hint_y=None)
        scroll.height = self.height*.6
        scroll.width = self.width
        scroll.add_widget(grid)
        box = GridLayout(cols=1)
        box.add_widget(scroll)
        return box
