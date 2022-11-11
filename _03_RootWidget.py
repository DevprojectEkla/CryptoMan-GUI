import os

from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.input.providers import mouse
from kivy.input.providers.mouse import MouseMotionEvent

from kivy.properties import StringProperty, BooleanProperty, ObjectProperty, ListProperty
from kivy.uix.screenmanager import Screen

from _03_ChoixFichierClef import ChoixFichierClef

""" ATTENTION l'import suivant est nécessaire bien que la classe ne soit pas appelée dans ce fichier python"""
from _03_ChargerClef import ChargerClef


class RootWidget(Screen):
    """Menu principal de l'application"""
    # le chemin d'accès vers le dossier où l'application est installée.
    app_path = os.path.dirname(os.path.abspath("_00_CryptoGUI.py"))
    # Différent flags et variables du fichier .kv TODO:à vérifier si les strings ici sont vraiment utiles
    TXT_charger = "Charger une clé"
    TXT_crypterfichier = "Crypter un fichier"
    key_display = StringProperty("")
    key_state = BooleanProperty(False)
    crypterFlag = BooleanProperty(False)
    key = StringProperty("Voici la clé qui sera utilisée dans cette session:")

    b_loadkey = ObjectProperty()
    boxchoix = ObjectProperty()
    canvas_KEY = ListProperty([0, 0, 0, 0])
    # nos variables popup
    img_popup = StringProperty()
    msg_popup = StringProperty()

    # variable concernant l'affichage de la fenêtre principale de l'app
    window_size = Window._get_system_size()
    full_screen = BooleanProperty()

    # variables pour gérer le son
    init = None
    sound_menu = None
    sound_encryption = None
    sound_decryption = None
    sound_chargement = None
    sound_choix = None
    sound_choix_fichier = None
    sound_choix_fichier2 = None
    sound_fichier_introuvable = None
    sound_key_maker = None
    sound_retour = None

    def chooseFile(self):
        self.boxchoix = ChoixFichierClef()
        self.add_widget(self.boxchoix)

    def set_key_state(self, widget):
        if widget.disabled:
            self.key_state = False
        else:
            self.key_state = True

    def reset_key_state(self):
        self.key_state = False

    def loadKey(self):
        """ATTENTION : utilisée dans le fichier.kv : simple print de deboggage"""
        print("loading a key")

    def keyloaded(self):
        """ATTENTION : utilisée dans le fichier.kv"""
        print("removing button keyload")
        self.remove_widget(self.b_loadkey)

    def setcrypterflag(self):
        """ATTENTION : utilisée dans le fichier.kv"""
        self.crypterFlag = True
        return True

    def init_audio(self):
        self.sound_menu = SoundLoader.load("audio/menu.wav")
        self.sound_retour = SoundLoader.load("audio/bouton_retour.wav")
        self.sound_encryption = SoundLoader.load("audio/cryptagefichier.wav")
        self.sound_decryption = SoundLoader.load("audio/decrypter_fichier.wav")
        self.sound_chargement = SoundLoader.load("audio/chargement.wav")
        self.sound_key_maker = SoundLoader.load("audio/keymaker.wav")
        self.sound_choix = SoundLoader.load("audio/choix.wav")
        self.sound_choix_fichier = SoundLoader.load("audio/choix_fichier.wav")
        self.sound_choix_fichier2 = SoundLoader.load("audio/choix_fichier2.wav")

        self.sound_fichier_introuvable = SoundLoader.load("audio/fichier_introuvable.wav")

        self.sound_menu.volume = 1
        self.sound_key_maker.volume = 1
        self.sound_retour.volume = 1
        self.sound_encryption.volume = .75
        self.sound_chargement.volume = .75
        self.sound_choix.volume = .75

    def close(self):
        """Ces méthodes sont appelées dans le fichier .kv"""
        Window.close()

    def minimize(self):
        Window.minimize()


    def reduce_size(self):
        print(self.window_size)
        if self.full_screen:

            self.full_screen = False
            Window.borderless = True
            Window.size = (800, 600)
            Window.fullscreen = False
        else:
            Window.size = tuple(self.window_size)
            Window.fullscreen = True
            self.full_screen = True
