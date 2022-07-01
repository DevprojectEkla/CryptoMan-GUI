from kivy.metrics import dp
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty, NumericProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import Screen

from _02_ChoixFichier import DossierIntrouvable, MyProgressBar, MyPopUp
from _03_ChoixDossierCrypter import ChoixDossierCrypter
from _02_Directory import Directory


class CrypterDossier(Screen):
    """Ecran d'affichage correspondant à l'option 'crypter un dossier' """
    key = StringProperty("")
    objetKey = ObjectProperty()
    dirname = StringProperty("")
    cryptageOK = BooleanProperty()
    boxchoix = ObjectProperty()
    boxask = ObjectProperty()
    b_state = BooleanProperty()
    progress_bar = ObjectProperty()
    progvalue = NumericProperty()
    pop = ObjectProperty()
    dossier_introuvable = ObjectProperty()
    initOK = BooleanProperty()
    d_introuvable = BooleanProperty()

    def initialiserChoix(self):
        self.clearbox()
        self.b_state = True
        self.d_introuvable = False
        self.cryptageOK = False
        self.boxchoix = ChoixDossierCrypter()
        self.add_widget(self.boxchoix)

    def clearbox(self):
        if self.dossier_introuvable:
            self.remove_widget(self.dossier_introuvable)

    def closeBoxChoix(self):
        print("closing choix")
        self.remove_widget(self.boxchoix)
        if self.d_introuvable:
            self.remove_widget(self.dossier_introuvable)
            self.b_state = False
        if self.boxask:
            self.remove_widget(self.boxask)

    def returnMenu(self):
        if self.boxchoix:
            self.remove_widget(self.boxchoix)
            self.b_state = False
        self.manager.current = "RootWidget"
        self.manager.transition.direction = "right"

    def closeChoixFichier(self):
        if self.cryptageOK:
            if self.boxchoix:
                self.remove_widget(self.boxchoix)
            if self.progress_bar:
                self.remove_widget(self.progress_bar)
            if self.pop:
                self.remove_widget(self.pop)
            self.returnMenu()
        else:
            if self.boxchoix:
                self.remove_widget(self.boxchoix)
            if self.progress_bar:
                self.remove_widget(self.progress_bar)
            if self.dossier_introuvable:
                self.remove_widget(self.dossier_introuvable)
            print("Error: Crypter@Screen =  S5: self.cryptageOk = False ")
            if self.d_introuvable:
                print("flag d_introuvable True dans closeChoixFichier de crypterDossier")
                self.initDossierIntrouvable()
            print("box choix fermée ok")
            print("le cryptage a échoué (en tout cas la variable cryptage_OK est False, "
                  "voir méthode closeChoixFichier dans le S5 CrypterDossier")
            print("Error:CrypterDossier@Screen =  S5: self.cryptageOk = False ")

    def crypterTerminated(self):
        if self.cryptageOK:
            self.afficherOK()
        else:
            self.closeChoixFichier()
            print(f"cryptage du fichier {self.dirname} terminé")

    def afficherOK(self):
        self.closeChoixFichier()
        self.pop = MyPopUp(title='Cryptage Réussi !', size_hint=(.3, .3))

        self.pop.open()

    def afficherProgressBar(self):
        if self.initOK:
            self.progress_bar = MyProgressBar()
            self.progvalue = self.progress_bar.value
            self.closeBoxChoix()

    def initDossierIntrouvable(self):
        """Appelée par closeChoixFichier. ATTENTION : On a eu recours à une astuce ici. On ajoute un bouton
        'Retour' par-dessus le bouton 'Retour' qui est déjà créé avec la classe fichierIntrouvable
         dans le fichier .kv car ce dernier est lié à l'écran S3 de l'opération crypter et ici on veut revenir sur
          l'écran S4 de l'opération décrypter."""
        self.dossier_introuvable = DossierIntrouvable()
        self.dossier_introuvable.init_box_introuvable()
        self.dossier_introuvable.b_back = Button(background_color=(0, 0, 0, 0), text='Retour',
                                                 font_name='Fonts/matrix regular.ttf', font_size=dp(30),
                                                 size_hint=(.5, .5), pos_hint={"center_x": .5, "center_y": .3})
        self.dossier_introuvable.b_back.bind(on_press=lambda args: self.closeBoxChoix())
        self.dossier_introuvable.add_widget(self.dossier_introuvable.b_back)
        print(f"print de self.introuvable dans initfichierintouvable de Crypterfichier: {self.d_introuvable}")
        self.d_introuvable = True
        self.dossier_introuvable.text = "ceci est un test dans decrypter fichier"
        self.add_widget(self.dossier_introuvable)
