import os
import threading
from pathlib import Path

from kivy.core.audio import SoundLoader
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy.uix.floatlayout import FloatLayout

from _01_AlgoG import AlgoG
from _02_ChoixFichier import FichierIntrouvable
from _02_File import File
from _02_KeyFile import Key


class ChoixFichierCrypter(FloatLayout):
    """Classe spéciale pour la fenêtre de choix de fichier à crypter. Attention il faut vérifier beaucoup de choses
    avec des demandes d'entrée utilisateur en fonction des cas rencontrés: 1) fichier inexistant, 2) fichier crypt_
    déjà présent sous le même nom dans le dossier d'arrivée etc."""
    app_path = os.path.dirname(os.path.abspath("_00_CryptoGUI.py"))
    algo = AlgoG()
    key = StringProperty("")
    objetKey = ObjectProperty()
    text = StringProperty("Entrez un nom de fichier à crypter:")
    createkeyFlag = BooleanProperty(False)
    crypterFlag = BooleanProperty(False)
    cryptageOK = BooleanProperty(False)
    b_state = BooleanProperty()
    fichierintrouvable = ObjectProperty()
    f_introuvable = BooleanProperty(False)
    overwrite = BooleanProperty(False)
    askoverwrite = BooleanProperty(False)
    file = ObjectProperty()
    cryptfile = ObjectProperty()
    sound_encryption = ObjectProperty()
    sound_enter = ObjectProperty()
    thread_sound_encryption = ObjectProperty()
    thread_sound_enter = ObjectProperty()

    def setFile(self, widget):
        os.chdir(self.app_path)
        if os.path.isfile(widget.text):
            path = Path(widget.text)
            self.file = File(path)
            return True
        else:
            self.text = "Fichier introuvable ou inexistant"
            self.f_introuvable = True
            self.b_state = True  # ici on veut maintenir les boutons de l'écran Crypterfichier sur Disabled car
            # la fenêtre fichier introuvable s'affiche et on veut que l'écran de cryptage reste inaccessible
            # jusqu'à ce que l'utilisateur appuie sur le bouton retour ou équivalent du widget FichierIntrouvable
            print("Erreur: ChoixFichierCrypter:\nfichier introuvable ou inexistant:"
                  "choisissez un chemin d'accès complet.")
            return False

    def checkCryptfile(self):
        """ ATTENTION: cette fonction sert de critère à une demande d'entrée utilisateur. """
        self.cryptfile = self.algo.addPrefixAndExtension(self.file)
        if self.cryptfile.checkOverwriteUI() == "overwrite":
            return True
        elif self.cryptfile.checkOverwriteUI() == "ask overwrite":
            self.askoverwrite = True
            self.cryptfile.closeFile()
            print("[*] Crypter suspended: asking overwrite [*]")
            return False
        else:
            print("sorry an error occured in: checkCryptfile() de ChoixFichierCrypter.")
            return False

    def crypter(self, widget):
        if self.setFile(widget):
            key = self.objetKey.key
            if self.checkCryptfile():
                self.thread_sound_encryption.start()
                self.algo.cryptFileOperation2(self.file, self.cryptfile, key)
                self.file.closeFile()
                self.cryptfile.closeFile()
                self.text = "cryptage réussi"
                self.cryptageOK = True
                self.b_state = False # c'est inutile normalement car un cryptage réussi renvoi sur le menu principal
                # mais on veut quand même réactiver les boutons de l'écran Crypter fichier au cas où...
                os.chdir(self.app_path)
            else:
                self.askoverwrite = True
                print("echec de cryptage")
                self.text = "cryptage impossible"
                self.cryptageOK = False
        else:
            ERRfile = File("ERROR.txt").writeBytes2(f"ERREUR FICHIER INTROUVABLE:\n"
                                                    f"Erreur, le fichier {widget.text} n'existe pas."
                                                    f"\n Ce fichier Error.txt est généré automatiquement"
                                                    f"lors d'un tentative de cryptage ou de décryptage d'un fichier"
                                                    f"dont le chemin d'accès n'a pas été reconnu comme valide".encode())

            self.file = ERRfile
            self.cryptfile = ERRfile
            self.f_introuvable = True
            self.b_state = True

    def init_audio(self):

        self.sound_encryption = SoundLoader.load("audio/cryptagefichier.wav")
        self.thread_sound_encryption = threading.Thread(target=self.sound_encryption.play())
        self.sound_enter = SoundLoader.load("audio/enter.wav")
        self.thread_sound_enter = threading.Thread(target=self.sound_enter.play())

        self.sound_encryption.volume = .75
        self.sound_enter.volume = .75


class AskOverwriteCrypter(FloatLayout):
    """Le procédé est complexe. On ne peut apparemment pas en faire une simple méthode de la classe ChoixFichierCrypter
     car il faut créer un nouveau widget et l'affichage se passe mieux si on supprime le widget ChoixFichier. Un popup
     pourrait peut-être résoudre le problème, mais ce type de widget est moins facilement customisable."""
    text = StringProperty()
    file = ObjectProperty()
    cryptfile = ObjectProperty()
    cryptageOK = BooleanProperty()
    objetKey = ObjectProperty()
    algo = AlgoG()

    def ecraserFichier(self):

        self.cryptfile = self.algo.addPrefixAndExtension(self.file)
        self.cryptfile.overwrite = True
        self.cryptageOK = True
        self.algo.cryptFileOperation2(self.file,self.cryptfile, self.objetKey.key)


if __name__ == "__main__":
    choix = ChoixFichierCrypter()
    file = File("test.key")

    key = Key("secret.key")
    choix.objetKey = key
    choix.file = file
    cryptfile = AlgoG.addPrefixToFile(file=file,prefix="crypt_")
    cryptfile.overwrite=True
    print(cryptfile.name)
    choix.cryptfile = cryptfile
    a= choix.crypter()