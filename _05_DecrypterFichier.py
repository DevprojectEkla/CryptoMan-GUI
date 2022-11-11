from kivy.metrics import dp
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

from _01_AlgoG import AlgoG
from _02_ChoixFichier import FichierIntrouvable, MyPopUp
from _02_File import File

from _03_ChoixFichierDecrypter import ChoixFichierDecrypter, AskOverwriteDecrypter


class DecrypterFichier(Screen):
    """Ecran d'affichage correspondant à l'option 'crypter un fichier' """
    key = StringProperty()
    objetKey = ObjectProperty()
    filename = StringProperty()
    decryptageOK = BooleanProperty()
    boxchoix = ObjectProperty()
    b_state = BooleanProperty()
    boxask = ObjectProperty()
    fichierintrouvable = ObjectProperty()
    file = ObjectProperty()
    existingfile = ObjectProperty()
    f_introuvable = BooleanProperty(False)
    askoverwrite = BooleanProperty(False)

    def initialiserChoix(self):

        self.b_state = True
        self.decryptageOK = False
        self.boxchoix = ChoixFichierDecrypter()
        self.boxchoix.initDecryptage()
        self.add_widget(self.boxchoix)

    def closeBoxChoix(self):
        """Cette méthode peut être appelée par choixfichiercrypter pour fermer la fenêtre de choix de fichier"""
        print("closing choix")
        self.remove_widget(self.boxchoix)
        if self.f_introuvable:
            self.remove_widget(self.fichierintrouvable)
            self.b_state = False
        if self.boxask and not self.askoverwrite:
            self.remove_widget(self.boxask)
            self.b_state = False

    def returnMenu(self):
        if self.boxchoix:
            self.remove_widget(self.boxchoix)
            self.b_state = False
        self.manager.current = "RootWidget"
        self.manager.transition.direction = "right"

    def setkey(self):
        self.key = StringProperty()
        pass

    def initfichierIntrouvable(self):
        """Appelée par closeChoixFichier. ATTENTION : On a eu recours à une astuce ici. On ajoute un bouton
        'Retour' par-dessus le bouton 'Retour' qui est déjà créé avec la classe fichierIntrouvable
         dans le fichier .kv car ce dernier est lié à l'écran S3 de l'opération crypter et ici on veut revenir sur
          l'écran S4 de l'opération décrypter."""
        self.fichierintrouvable = FichierIntrouvable()
        self.fichierintrouvable.init_box_introuvable()
        self.fichierintrouvable.b_back = Button(background_color= (0, 0, 0, 0),text='Retour',
                                                font_name='Fonts/matrix regular.ttf', font_size= dp(30),
                                                size_hint=(.5, .5), pos_hint={"center_x": .5, "center_y": .3})
        self.fichierintrouvable.b_back.bind(on_press=lambda args : self.closeBoxChoix())
        self.fichierintrouvable.add_widget(self.fichierintrouvable.b_back)
        print(f"print de self.introuvable dans initfichierintouvable de Crypterfichier: {self.f_introuvable}")
        self.f_introuvable = True
        self.fichierintrouvable.text = "ceci est un test dans decrypter fichier"
        self.add_widget(self.fichierintrouvable)

    def closeChoixFichier(self):
        if self.decryptageOK:
            self.remove_widget(self.boxchoix)
            self.returnMenu()
        else:
            self.remove_widget(self.boxchoix)
            if self.boxask and not self.askoverwrite:
                self.remove_widget(self.boxask)
                self.b_state = False
                print("boxaskoverwrite fermée")
            if self.f_introuvable:
                print("flag f_introuvable True dans closeChoixFichier de CrypterFIchier")
                self.initfichierIntrouvable()
            print("box choix fermée ok")
            print("Error in DecrypteFichierr@Screen in closeChoixFichier() S4: self.decryptageOk = False ")

    def afficherOK(self):
        self.closeBoxChoix()
        pop = MyPopUp(title='Décryptage Réussi !', size_hint=(.3, .3))
        pop.open()

    def afficherERREUR(self):
        self.closeBoxChoix()
        content = GridLayout(cols=1)
        content_b_OK = Button(text='OK', size_hint_y=None, height=40)
        content.add_widget(Label(text=f"le fichier {self.filename} n'a pas pu être décrypté"))
        content.add_widget(content_b_OK)
        pop = Popup(title='Echec du Décryptage  !',
                    content=content, size_hint=(.3, .3))
        content_b_OK.bind(on_release=pop.dismiss)
        pop.open()

    def askOverwrite(self):
        if self.askoverwrite:
            self.boxask = AskOverwriteDecrypter()
            self.boxask.text = f"voulez-vous écraser le fichier existant:{self.existingfile.name}"
            self.add_widget(self.boxask)

    def decrypterTerminated(self):
        if self.decryptageOK:
            self.afficherOK()
        elif self.f_introuvable or self.askoverwrite:
            pass
        else:
            self.afficherERREUR()
        self.closeChoixFichier()
        print(f"decryptage du fichier {self.filename} terminé.")


