from kivy.core.audio import SoundLoader
from kivy.properties import BooleanProperty, StringProperty, ObjectProperty
from kivy.uix.screenmanager import Screen

from _01_AlgoG import AlgoG
from _02_KeyFile import Key
from _03_ChoixFichierClef import ChoixFichierClef


class ChargerClef(Screen):
    """Classe pour la fenêtre de chargement du fichier .key"""
    b_state = BooleanProperty(False)
    algo = AlgoG()
    loadedkey = ObjectProperty(Key())
    key = StringProperty("")
    boxchoix = ObjectProperty()
    createkeyFlag = BooleanProperty(False)
    crypterFlag = BooleanProperty(False)
    sound_choix = None

    def exclude(self):
        if self.crypterFlag:
            self.createkeyFlag = False

    def closeBoxChoix(self):
        print("closing choix")
        self.remove_widget(self.boxchoix)

    def closeChoixFichier(self):
        if self.key:
            self.remove_widget(self.boxchoix)
            self.sound_choix.play()
            self.returnMenu()
        else:
            print("It didn't return a key")

    def loadkey(self):
        print("loading the file 'secret.key'")
        self.key = str(self.loadedkey.key)

    def create_new_key(self):
        print("creating new key file")
        self.key = self.algo.creationNouveauFichierGUI()
        self.closeChoixFichier()

    def chooseFile(self):
        self.boxchoix = ChoixFichierClef()
        self.add_widget(self.boxchoix)

    def setkey(self):
        pass

    def returnMenu(self):
        if self.boxchoix:
            self.remove_widget(self.boxchoix)
            self.b_state = False
        self.manager.current = "RootWidget"
        self.manager.transition.direction = "right"

    def init_audio(self):
        self.sound_choix = SoundLoader.load("audio/choix.wav")
