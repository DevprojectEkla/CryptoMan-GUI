import os
import threading
from pathlib import Path

from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.properties import StringProperty, ObjectProperty, ListProperty, BooleanProperty
from kivy.uix.floatlayout import FloatLayout

from _01_AlgoG import AlgoG
from _02_Directory import Directory


class ChoixDossierDecrypter(FloatLayout):
    """Classe spéciale pour la fenêtre de choix de fichier à crypter"""
    app_path = os.path.dirname(os.path.abspath("_00_CryptoGUI.py"))
    algo = AlgoG()
    key = StringProperty("")
    objetKey = ObjectProperty()
    srcDir = ObjectProperty()
    path = ObjectProperty()
    dirname = StringProperty()
    fileList = ListProperty()
    subdirList = ListProperty()
    text = StringProperty("Entrez un nom de dossier à décrypter")
    createkeyFlag = BooleanProperty(False)
    crypterFlag = BooleanProperty(False)
    decryptageOK = BooleanProperty(False)
    b_state = BooleanProperty()
    d_introuvable = BooleanProperty()
    initOK = BooleanProperty()

    sound_decryption = None
    sound_enter = None
    thread_sound_decryption = ObjectProperty()
    thread_sound_enter = None

    def initDirectory(self, widget):
        """Initialisation du dossier à décrypter : commence par une boucle de choix pour la sélection du fichier puis
        fixe les valeurs des variables de la class qui serviront en argument de la fonction crypter(). Il faut
        lancer initFichier avant chaque opération de décryptage si la classe n'est pas réinstancié entre deux
        utilisations de décrypter()"""
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
            self.d_introuvable = True
            self.b_state = True
            print("Erreur: ChoixDossierDecrypter:\ndossier introuvable ou inexistant:"
                  "choisissez un chemin d'accès complet.")

    def decrypter(self):
        if self.initOK:
            key = self.objetKey.key
            try:
                Window.minimize()
                self.thread_sound_decryption.start()

                # décryptage du dossier :
                self.algo.decryptDirectoryOperation(self.fileList, key)
                os.chdir(self.app_path)  # on doit retourner dans le dossier de l'application après cette opération
                # Sinon l'appli ne sait pas retrouver le chemin vers les images du popup "decryptage réussi".
                # On ferme le thread proprement de cette manière :
                self.thread_sound_decryption.join()
                Window.restore()
                # on peut libérer l'application en utilisant un thread séparé mais le popup 'Decryptage réussi
                # s'affiche aussitôt alors que l'opération est encore en cours.
                # thread = Thread(target=self.algo.decryptDirectoryOperation, args=(self.fileList, key))
                # thread.start()
                self.text = f"décryptage dossier {self.dirname} réussi"
                self.decryptageOK = True
            except:
                print("echec de cryptage du dossier")
                self.text = "décryptage dossier impossible"
                self.decryptageOK = False

        else:
            # TODO: insérer ici le flag self.f_dossierintrouvable
            self.d_introuvable = True
            self.decryptageOK = False
            print("le dossier n'a pas été initialisé correctement: dossier introuvable")

    def init_audio(self):

        self.sound_decryption = SoundLoader.load("audio/decryptage_dossier.wav")
        self.thread_sound_decryption = threading.Thread(target=self.sound_decryption.play())
        self.sound_enter = SoundLoader.load("audio/enter.wav")
        self.thread_sound_enter = threading.Thread(target=self.sound_enter.play())

        self.sound_decryption.volume = .75
        self.sound_enter.volume = .75