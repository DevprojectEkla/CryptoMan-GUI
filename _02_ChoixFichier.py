from kivy.core import window
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import StringProperty, BooleanProperty, ObjectProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar

from _01_AlgoG import AlgoG

""" Toutes les classes suivantes sont le pendant python des classes définies dans le fichier .kv"""


class ChoixFichier(FloatLayout):
    """Classe générale pour la fenêtre de choix de fichier"""
    algo = AlgoG()
    key = StringProperty("")
    text = StringProperty("")
    createkeyFlag = BooleanProperty(False)
    crypterFlag = BooleanProperty(False)

    def close(self):
        self.close()

    def minimize(self):
        self.minimize()


class FichierIntrouvable(FloatLayout):
    text = "Fichier Introuvable"
    b_state = BooleanProperty()
    b_back = ObjectProperty()

    def init_box_introuvable(self):
        self.b_back = Button(text='Retour', font_size=dp(25), font_name='Fonts/matrix regular.ttf')


class DossierIntrouvable(FloatLayout):
    text = "Dossier Introuvable"
    b_state = BooleanProperty()
    b_back = ObjectProperty()

    def init_box_introuvable(self):
        self.b_back = Button(text='Retour', font_size=dp(25), font_name='Fonts/matrix regular.ttf')


class MyPopUp(Popup):
    title = StringProperty()
    content = ObjectProperty()


class MyProgressBar(FloatLayout):
    pgb = ProgressBar()
    pgb.max = 100
    value = pgb.value

    def initPGB(self):
        self.add_widget(self.pgb)


class WindowBar(BoxLayout):
    img = StringProperty('img/window_reduire.png')

    def change_img_window(self):
        if self.img == 'img/window_reduire.png':
            self.img = 'img/window_agrandir.png'
        else:
            self.img = 'img/window_reduire.png'
