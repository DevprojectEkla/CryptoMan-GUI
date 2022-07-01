from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

from _03_ChoixFichierCrypter import ChoixFichierCrypter, AskOverwriteCrypter
from _02_ChoixFichier import FichierIntrouvable, MyPopUp
from _02_File import File


class CrypterFichier(Screen):
    """Ecran d'affichage correspondant à l'option 'crypter un fichier' """
    key = StringProperty("")
    objetKey = ObjectProperty()
    filename = StringProperty("")
    boxchoix = ObjectProperty()
    boxask = ObjectProperty()
    fichierintrouvable = ObjectProperty()
    file = ObjectProperty()
    existingfile = ObjectProperty()
    cryptageOK = BooleanProperty(False)
    b_state = BooleanProperty(True)
    f_introuvable = BooleanProperty(False)
    askoverwrite = BooleanProperty(False)

    def initialiserChoix(self):
        """ Cette méthode est appelée dans le fichier .kv par RootWidget pour initialiser tout de suite un choix
        de fichier"""
        self.b_state = True
        self.f_introuvable = False
        self.clearbox()
        self.boxchoix = ChoixFichierCrypter()
        self.add_widget(self.boxchoix)

    def closeBoxChoix(self):
        """Cette méthode peut être appelée par choixfichiercrypter pour fermer la fenêtre de choix de fichier"""
        print("closing choix")
        self.remove_widget(self.boxchoix)
        if self.f_introuvable:
            self.remove_widget(self.fichierintrouvable)
        if self.boxask:
            self.remove_widget(self.boxask)

    def returnMenu(self):
        """c'est la méthode aussi bien du bouton retour que celle qui est appelée après une opération de cryptage
        réussie avec retour automatique au menu principal. Elle n'est pas appelée directement mais par la méthode
        closeChoixFichier"""
        if self.boxchoix:
            self.remove_widget(self.boxchoix)
            self.b_state = False
        self.manager.current = "RootWidget"
        self.manager.transition.direction = "right"

    def closeChoixFichier(self):
        """appelée dans le fichier .kv par ChoixFichierCrypter après une tentative de cryptage"""
        if self.cryptageOK:
            self.remove_widget(self.boxchoix)
            self.returnMenu()
        else:
            self.remove_widget(self.boxchoix)
            if self.f_introuvable:
                print("flag f_introuvable True dans closeChoixFichier de CrypterFIchier")
                self.initfichierIntrouvable()
            print("box choix fermée ok")
            print("le cryptage a échoué (en tout cas la variable cryptage_OK est False, voir méthode closeChoixFichie"
                  "dans le S3 Crypter fichier")

    def checkIntrouvable(self):
        if self.f_introuvable:
            self.remove_widget(self.boxchoix)
            self.initfichierIntrouvable()

    def clearbox(self):
        if self.fichierintrouvable:
            self.remove_widget(self.fichierintrouvable)

    def initfichierIntrouvable(self):
        """appelée par closeChoixFichier"""
        self.fichierintrouvable = FichierIntrouvable()
        print(f"print de self.introuvable dans initfichierintouvable de Crypterfichier: {self.f_introuvable}")
        self.f_introuvable = True
        self.fichierintrouvable.text = "ceci est un test dans crypter fichier"
        self.add_widget(self.fichierintrouvable)

    def askOverwrite(self):
        if self.askoverwrite:
            self.boxask = AskOverwriteCrypter()
            self.boxask.text = f"voulez-vous écraser le fichier existant:{self.existingfile.name}"
            self.add_widget(self.boxask)

    def afficherOK(self):
        self.closeBoxChoix()
        pop = MyPopUp(title='Cryptage Réussi !', size_hint=(.3, .3))
        pop.open()

    def crypterTerminated(self):
        if self.cryptageOK:
            self.afficherOK()
        self.closeChoixFichier()
        print(f"cryptage du fichier {self.filename} terminée")

    def close(self):
        self.closeBoxChoix()

    def minimize(self):
        self.closeBoxChoix()
