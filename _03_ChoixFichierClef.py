from kivy.core.audio import SoundLoader
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, NumericProperty
from kivy.uix.floatlayout import FloatLayout

from _01_AlgoG import AlgoG
from _02_KeyFile import Key


class ChoixFichierClef(FloatLayout):
    """Classe spéciale pour la fenêtre de choix de fichier de clé de cryptage"""
    algo = AlgoG()
    key = StringProperty("")
    objetKey = ObjectProperty()
    text = StringProperty("Entrez un nom de fichier .key:")
    createkeyFlag = BooleanProperty(False)
    crypterFlag = BooleanProperty(False)
    Label_color = ObjectProperty((0.3, 0.7, 0.5, 1))

    def exclude(self):
        if self.crypterFlag:
            self.createkeyFlag = True
        else:
            pass

    def loadkeyfile(self, widget):
        # widget.text: nom du fichier
        # chooseOther... fonction qui retourne un objet Key
        if not self.createkeyFlag:
            key = self.algo.chooseOtherFileGUI(widget.text)
            if key:
                self.objetKey = Key(widget.text)
                self.key = str(self.objetKey.key)
            else:
                self.Label_color = (0.9, .3, .3, 1)
                self.text = "fichier non valide"
        else:
            key = self.algo.creationNouveauFichierGUI(widget.text)
            if key:
                self.objetKey = key
                print(f"objetkey: {self.objetKey} et la clé est: {self.objetKey.key}")
                self.key = str(key.key)
            else:
                self.text = "Trying generating new key file Failed"
        return self.key

    def crypter(self):
        if self.crypterFlag:
            print("cryptage en cours")

    def checkkey(self, widget):
        pass
