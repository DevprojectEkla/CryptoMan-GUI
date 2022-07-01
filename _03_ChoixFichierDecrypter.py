import os
import threading
from pathlib import Path

from kivy.core.audio import SoundLoader
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy.uix.floatlayout import FloatLayout

from _01_AlgoG import AlgoG
from _02_File import File


class ChoixFichierDecrypter(FloatLayout):
    """Classe spéciale pour la fenêtre de choix de fichier à crypter"""
    app_path = os.path.dirname(os.path.abspath("_00_CryptoGUI.py"))
    algo = AlgoG()
    key = StringProperty()
    objetKey = ObjectProperty()  # attention ce n'est pas facile à manier, mais ça marche.
    text = StringProperty()
    createkeyFlag = BooleanProperty()
    decrypterFlag = BooleanProperty()
    decryptageOK = BooleanProperty()
    fichierintrouvable = ObjectProperty()
    f_introuvable = BooleanProperty(False)
    askoverwrite = BooleanProperty(False)
    file = ObjectProperty()
    decryptfile = ObjectProperty()
    b_state = BooleanProperty()
    sound_decryption = None
    sound_enter = None
    thread_sound_decryption = ObjectProperty()
    thread_sound_enter = None

    def initDecryptage(self):
        os.chdir(self.app_path)
        self.createkeyFlag = False
        self.decrypterFlag = False
        self.decryptageOK = False
        self.text = "Entrez un nom de fichier à décrypter"

    def setFile(self, widget):
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
            print("Erreur setFile() methode de ChoixFichierDecrypter:\nfichier introuvable ou inexistant:"
                  "choisissez un chemin d'accès complet.")
            return False

    def checkDecryptfile(self):
        """ ATTENTION: cette fonction sert de critère à une demande d'entrée utilisateur. """
        if "crypt_" in self.file.name:
            self.decryptfile = File(self.file.path.parent/self.algo.delPrefix(self.file.name,"crypt_"))
        else:
            self.decryptfile = File(self.file.path)
        if self.decryptfile.checkOverwriteUI() == "overwrite":
            return True
        elif self.decryptfile.checkOverwriteUI() == "ask overwrite":
            self.askoverwrite = True
            self.decryptfile.closeFile()
            print("[*] Decrypt operation suspended: asking overwrite [*]")
            return False
        else:
            print("sorry an error occured in: checkDecryptfile() de ChoixFichierDecrypter.")
            return False

    def decrypter(self,widget):
        if self.setFile(widget):
            key = self.objetKey.key
            if self.checkDecryptfile():
                self.thread_sound_decryption.start()
                self.algo.decryptFileOperation2(self.file, self.decryptfile, key)
                os.chdir(self.app_path)
                self.file.closeFile()
                self.decryptfile.closeFile()
                self.text = "decryptage réussi"
                self.decryptageOK = True
                self.b_state = False  # c'est inutile normalement car un cryptage réussi renvoi sur le menu principal
                # mais on veut quand même réactiver les boutons de l'écran Crypter fichier au cas où...
            else:
                self.askoverwrite = True
                print("echec de decryptage")
                self.text = "decryptage impossible"
                self.decryptageOK = False

        else:
            """ATTENTION: Pour une raison inexplicable on ne peut pas se permettre de ramener la variable self.file
            ou self.decryptfile à None, cela déclenche l'erreur: BaseException Decrypter.file is not allowed to be None
            il faut donc retourner un fichier bidon à l'écran S4 pour que ses variables self.file et self.decryptfile
            reçoivent une instance de la classe File.
            NB: l'erreur ne se déclenche que dans le cas où la classe File a bien été instancié une première fois
            par un vrai fichier. Si l'utilisateur entre un mauvais nom de fichier dès le départ l'erreur n'est pas levée
            mais si l'utilisateur fait un premier essai avec un vrai nom de fichier l'erreur sera levée la fois suivante
            s'il entre un nom de fichier inexistant."""
            ERRfile = File("error.txt").writeBytes2(f"Erreur, le fichier {widget.text} n'existe pas".encode())
            self.file = ERRfile
            self.decryptfile = ERRfile
            self.f_introuvable = True
            self.b_state = True

    def init_audio(self):

        self.sound_decryption = SoundLoader.load("audio/decrypter_fichier.wav")
        self.thread_sound_decryption = threading.Thread(target=self.sound_decryption.play())
        self.sound_enter = SoundLoader.load("audio/enter.wav")
        self.thread_sound_enter = threading.Thread(target=self.sound_enter.play())

        self.sound_decryption.volume = .75
        self.sound_enter.volume = .75


class AskOverwriteDecrypter(FloatLayout):
    """Le procédé est complexe. On ne peut apparemment pas en faire une simple méthode de la classe ChoixFichierCrypter
     car il faut créer un nouveau widget et l'affichage se passe mieux si on supprime le widget ChoixFichier. Un popup
     pourrait peut-être résoudre le problème, mais ce type de widget est moins facilement customisable."""
    text = StringProperty()
    file = ObjectProperty()
    decryptfile = ObjectProperty()
    decryptageOK = BooleanProperty()
    objetKey = ObjectProperty()
    askoverwrite = BooleanProperty()
    sound_decryption = ObjectProperty()
    thread_sound_decryption = ObjectProperty()
    algo = AlgoG()

    def init_audio(self):

        self.sound_decryption = SoundLoader.load("audio/decrypter_fichier.wav")
        self.thread_sound_decryption = threading.Thread(target=self.sound_decryption.play())

    def ecraserFichier(self):
        """L'algo est un peu coûteux car au final on effectue deux fois le décryptage on pourrait récupérer le
        contenu décrypter et effectuer ici la simple opération d'écrire ce contenu au lieu de relancer la même fonction
        decryptFile..."""
        if "crypt_" in self.file.name:
            self.decryptfile = File(self.file.path.parent/self.algo.delPrefix(self.file.name,"crypt_"))
        else:
            self.decryptfile = File(self.file.path)
        # initialisation des flag pour écraser le fichier
        self.decryptfile.overwrite = True
        self.decryptageOK = True
        self.askoverwrite = False
        # thread du son start:
        self.thread_sound_decryption.start()
        # décryptage et écriture dans le fichier
        self.algo.decryptFileOperation2(self.file, self.decryptfile, self.objetKey.key)


