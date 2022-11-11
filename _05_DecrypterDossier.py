from kivy.graphics import Canvas, Color, Rectangle
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

from _02_ChoixFichier import DossierIntrouvable, MyPopUp
from _03_ChoixDossierDecrypter import ChoixDossierDecrypter


class DecrypterDossier(Screen):
    """Ecran d'affichage correspondant à l'option 'crypter un fichier' """
    key = StringProperty("")
    objetKey = ObjectProperty()
    dirname = StringProperty("")
    decryptageOK = BooleanProperty(False)
    boxchoix = ObjectProperty()
    boxask = ObjectProperty()
    b_state = BooleanProperty(True)
    pop = ObjectProperty()
    dossier_introuvable = ObjectProperty()
    d_introuvable = BooleanProperty()

    def initialiserChoix(self):
        self.clearbox()
        self.b_state = True
        self.d_introuvable = False
        self.boxchoix = ChoixDossierDecrypter()
        self.add_widget(self.boxchoix)

    def clearbox(self):
        if self.dossier_introuvable:
            self.remove_widget(self.dossier_introuvable)

    def closeBoxChoix(self):
        """Cette méthode peut être appelée par choixfichiercrypter pour fermer la fenêtre de choix de fichier"""
        print("closing choix")
        self.remove_widget(self.boxchoix)
        if self.d_introuvable:
            self.remove_widget(self.dossier_introuvable)
        if self.boxask:
            self.remove_widget(self.boxask)

    def returnMenu(self):
        if self.boxchoix:
            self.remove_widget(self.boxchoix)
            self.b_state = False
        self.manager.current = "RootWidget"
        self.manager.transition.direction = "right"

    def closeChoixFichier(self):
        # TODO: renommer en closeChoixDossier
        if self.decryptageOK:
            self.remove_widget(self.boxchoix)
            if self.pop:
                self.remove_widget(self.pop)
            self.returnMenu()
        else:
            self.remove_widget(self.boxchoix)
            if self.dossier_introuvable:
                self.remove_widget(self.dossier_introuvable)
            print("Error:Decrypter@Screen =  S6: self.decryptageOk = False ")
            if self.d_introuvable:
                print("flag d_introuvable True dans closeChoixFichier de DecrypterDossier")
                self.initDossierIntrouvable()
            print("box choix fermée ok")
            print("le decryptage a échoué (en tout cas la variable decryptage_OK est False, "
                  "voir méthode closeChoixFichie dans le S6 DecrypterDossier")

    def decrypterTerminated(self):
        if self.decryptageOK:
            self.afficherOK()
        else:
            self.closeChoixFichier()
        print(f"decryptage du dossier {self.dirname} terminé.")

    def afficherOK(self):
        self.closeChoixFichier()
        # content = GridLayout(cols=1)
        # content_b_OK = Button(text='OK', size_hint_y=None, height=40)
        # content.add_widget(Label(text=f'le dossier {self.dirname} a bien été décrypté'))
        # content.add_widget(content_b_OK)
        self.pop = MyPopUp(title=" Décryptage réussi",size_hint=(.3, .3))
        self.pop.opacity = 1
        # content_b_OK.bind(on_release=self.pop.dismiss)
        self.pop.open()

    def initDossierIntrouvable(self):
        """appelée par closeChoixFichier"""
        self.dossier_introuvable = DossierIntrouvable()
        print(f"print de self.introuvable dans initDossierIntouvable de Crypterfichier: {self.d_introuvable}")
        self.d_introuvable = True
        self.dossier_introuvable.text = "ceci est un test dans crypter fichier"
        self.add_widget(self.dossier_introuvable)

