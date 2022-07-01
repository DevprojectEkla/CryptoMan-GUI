import os
import threading
from pathlib import Path

from kivy.core.audio import SoundLoader
from kivy.core.window import Window

from kivy.properties import StringProperty, ObjectProperty, ListProperty, BooleanProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.progressbar import ProgressBar


from _01_AlgoG import AlgoG
from _02_Directory import Directory


class ChoixDossierCrypter(FloatLayout):
    """Classe spéciale pour la fenêtre de choix de dossier à crypter"""
    app_path = os.path.dirname(os.path.abspath("_00_CryptoGUI.py"))
    algo = AlgoG()
    key = StringProperty("")
    objetKey = ObjectProperty()
    srcDir = ObjectProperty()
    path = ObjectProperty()
    dirname = StringProperty()
    fileList = ListProperty()
    subdirList = ListProperty()
    text = StringProperty("Entrez un nom de dossier à crypter")
    createkeyFlag = BooleanProperty(False)
    crypterFlag = BooleanProperty(False)
    cryptageOK = BooleanProperty(False)
    b_state = BooleanProperty()
    d_introuvable = BooleanProperty()
    initOK = BooleanProperty()

    sound_encryption = ObjectProperty()
    sound_enter = ObjectProperty()
    thread_sound_encryption = ObjectProperty()
    thread_sound_enter = ObjectProperty()

    def initDirectory(self, widget):
        """Initialisation du dossier à crypter : commence par une boucle de choix pour la sélection du fichier puis
        fixe les valeurs des variables de la class qui serviront en argument de la fonction crypter(). Il faut
        lancer initFichier avant chaque opération de cryptage si la classe n'est pas réinstancié entre deux
        utilisations de crypter()"""
        os.chdir(self.app_path)
        if os.path.isdir(widget.text):
            self.path = Path(widget.text)
            self.srcDir = Directory(self.path)
            self.fileList = self.srcDir.treeFileList
            self.subdirList = self.srcDir.treeSubdirList
            self.dirname = self.path.name
            print(self.fileList)
            self.initOK = True
        else:
            self.initOK = False

    def crypter(self):
        key = self.objetKey.key
        if self.initOK:
            try:
                self.thread_sound_encryption.start()
                Window.minimize()
                self.algo.cryptDirectoryOperation(self.fileList, key)
                os.chdir(self.app_path)  # on doit ensuite revenir au dossier de l'appli pour retrouver les bons chemins
                # d'accès vers nos images.
                self.thread_sound_encryption.join()
                # on peut créer un nouveau thread pour rendre aussitôt la main, mais attention, car l'utilisateur
                # pourrait ne pas comprendre que l'opération est en cours :
                # thread = Thread(target=self.algo.cryptDirectoryOperation, args=(self.fileList, key))
                # thread.start()
                Window.restore()
                self.text = f"cryptage dossier {self.dirname} réussi"
                self.cryptageOK = True
            except:
                print("echec de cryptage du dossier")
                self.text = "cryptage dossier impossible: choisissez un chemin complet vers un dossier existant"
                self.cryptageOK = False
        else:
            self.d_introuvable = True
            self.cryptageOK = False
            print("le dossier n'a pas été initialisé correctement: dossier introuvable")

    def afficherProgressBar(self):
        self.progress = ProgressBar()
        self.progress.max = 100
        self.progress.size_hint = (1, 1)
        self.progress.pos_hint = {"center_x": 1, "center_y": 1}
        self.progvalue = self.progress.value
        self.add_widget(self.progress)

    def incrementBar(self):
        self.progress.value += 1
        pass

    def init_audio(self):

        self.sound_encryption = SoundLoader.load("audio/cryptage_dossier.wav")
        self.thread_sound_encryption = threading.Thread(target=self.sound_encryption.play())
        self.sound_enter = SoundLoader.load("audio/enter.wav")
        self.thread_sound_enter = threading.Thread(target=self.sound_enter.play())

        self.sound_encryption.volume = .75
        self.sound_enter.volume = .75
