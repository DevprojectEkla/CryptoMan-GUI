"""importation des modules natifs usuels"""
import os
import random
import threading
from multiprocessing import Pool  # essaie pour la fonction extractBytesAndEncrypt
from crypt_message import read_bytes
'''modules publics non natifs plus spécifiques '''

'''modules personnels'''
from _01_general import *
from _02_Classes import *
from _02_File import File
from _02_KeyFile import Key
from _02_Choix import ChoixFichier


class AlgoG:
    """ Les méthodes algos de cette classe sont souvent très spécifiques à l'appli malgré leur nom un peu général,
     il ne faut pas croire qu'on puisse les reprendre dans d'autres applis comme c'est le cas des fonctions du module
    _01_general.py """

    def __init__(self):
        self.app_path = os.path.dirname(os.path.abspath("_00_CryptoGUI.py"))
        self.flag = None
        self.fichier = File  # on instancie pas encore la classe car on n'a pas de nom de chemin
        self.key = Key
        self.path = ""
        self.name = ""
        self.parent = ""

    def initFileVariables(self, name):
        """Instanciation de l'attribut self.fichier pour effectuer des opérations sur un fichier"""
        self.fichier = self.fichier(name)
        self.path = self.fichier.path
        self.name = self.fichier.name  # attention ici on appelle la propriété de File() une fois que self.fichier est
        # instancié

    @staticmethod
    def presentation():
        try:
            print(f"\n{open('Readme.txt', 'r').read()}")

        except:
            print("Exception: could not find the presentation File")
            time.sleep(1)
            print("\n\n\tCrypto v.1.0: This is a simple program to encrypt and decrypt a text file."
                  "\n\tby Fr. Raphael Boralevi")

    @staticmethod
    def read_bytes(file):
        try:
            content = Path(file).read_bytes()
        except:
            content = Path(file).read_text()
        return content

    def initKeyVariables(self, name):
        '''instanciation de l'attribut self.key pour effectuer des opérations sur un fichier clé à partir de l'objet
        Key(name)'''
        self.key = self.key(name)

    @staticmethod
    def encryptAnyContent(content, key):
        """Encrypts any type of content. Attention ici on veut garder des paramètres qui ne soient pas des attributs de
        la classe car on veut pouvoir appeller cette méthode dans d'autres modules sur des variables locales"""
        if isinstance(content, str):
            content = content.encode("Utf8")
        f = Fernet(key)
        try:
            encrypted_content = f.encrypt(content)  # cet appel est propre au module fernet
            return encrypted_content
        except:
            print("CryptAnyContent: fernet.encrypt failed for this content")
            return False


    @staticmethod
    def decryptAnyContent(content, key):
        """Decrypts any kind of content, même remarque que plus haut pour les paramètres """
        if isinstance(content, str):
            content = content.encode("Utf8")
        f = Fernet(key)
        try:
            decrypted_content = f.decrypt(content)
            return decrypted_content
        except:
            print("DecryptAnyContent: fernet.decrypt failed for this content")
            return False

    @staticmethod
    def goodbye():
        try:
            print(open("goodbye.txt", "r").read())
        except:
            print("\n\t could not open file Goodbye.txt")
            print("\n\tGoodbye, thanks for using Cryptoman hope you enjoyed it.")
        sys.exit(0)

    @staticmethod
    def choiceOverWrite(name='secret.key'):
        key = Key(name)
        key.tryOverWrite()
        if key.key:
            return key
        else:
            return False

    @staticmethod
    def chooseOtherFile():
        '''ici on doit d'abord choisir le fichier contenant la clé à utiliser, il faut s'assurer que le fichier choisit
        contient bien une clé de cryptage Fernet.
        On instancie un objet ChoixFichier pour contraindre le choix d'un fichier à extension .key
        on retourne ensuite par cette fonctino le résultat de la méthode chooseotherKeyFile qui doit renvoyer un objet
        de la classe Key (et non pas la string de la clé)'''
        otherkeyfile = ChoixFichier('.key')
        return otherkeyfile.chooseOtherKeyFile()  # cette méthode de la classe ChoixfIchier est copieuse mais ça marche.

    @staticmethod
    def chooseOtherFileGUI(filename):
        if os.path.isfile(filename):
            key = Key(filename)
            if key.checkFernet():  # on vérifie que le fichier contient une clé utilisable par Fernet
                print(f"\n\tYou extracted a key from the file {filename} this is the key you will use in this session:"
                      f"\n\n\t\t{key.key}")
                return key
            else:
                print("the file is not a valid .key file")
        else:
            print("choose an existing file")

    def creationNouveauFichierGUI(self, newfile):
        if not os.path.isfile(newfile):
            key = self.key(newfile)
            key.initNewKeyFile()  # methode qui écris la clé dans le nouveau fichier
            print(f"\n\tYou created a key and saved it in the file: {newfile}.\n"
                  f"this is the key you will use in this session:\n\n\t\t{key.key}.\n\t")
            return key
        else:
            print("ERREUR: Probablement dû à l'existence d'un fichier de même nom "
                  "Attention: ce CODE n'esT PAS ENCORE PRET dans AlgoG.creationNnouveauFichierGUI()")

    def creationNouveauFichier(self):
        """Attention : Ce n'est pas une fonction générale TODO: réfléchir à un autre nom et emplacement.
        TODO: peut-être à déplacer dans ChoixFichier sous le nom creationNouveauFichierClef?
        ici on veut créer un nouveau fichier clé dont on demande d'abord le nom à l'utilisateur.
        On se sert de l'instance de ChoixFichier pour demander un nom de fichier. Il faut vérifier que le nom de fichier
        ne correspond pas déjà à un fichier existant et que l'extension de fichier choisie est la bonne à savoir .key
        c'est la méthode validerCreationFichier qui fait ce travail. Après quoi on instancie un objet Key et on appelle
        une méthode qui génère et écrit la nouvelle clé dans le fichier"""
        instanceChoix = ChoixFichier('.key')
        instanceChoix.question = "Entrez un nom pour la création du nouveau fichier clé"
        newfile = instanceChoix.validerCreationFichier()  # par cette méthode on s'assure de la création
        # d'un nouveau fichier pour lequel on a effectué une vérification d'extension.
        key = self.key(newfile)
        key.initNewKeyFile()  # methode qui écris la clé dans le nouveau fichier
        print(f"\n\tYou created a key and saved it in the file: {newfile}.\n"
              f"this is the key you will use in this session:\n\n\t\t{key.key}.\n\t")
        return key

    def loadKey(self, name):
        '''ici l'utilisateur veut charger le fichier par défaut 'secret.key'. Il faut tout de même s'assurer qu'il
        s'agit bien d'un fichier contenant une clé de cryptage ce que fait la méthode loadkey de la classe Key'''
        key = self.key(name)
        if key.loadKey():
            print(f"\n\tthis is the current key you will use in this session: {key.key},\n\t")
            return key
        else:
            print("the secret.key file has been corrupted please generate a new secret.key by choosing 'ovw'.")
            time.sleep(1)
            return False
    @staticmethod
    def addPrefixToFile(file:File, prefix="crypt_"):
        """ Cette fonction ajoute un prefixe directement au nom d'un objet de la classe File et renvoie un autre objet
         de la classe File avec le nouveau nom de fihcier"""
        newname = prefix + file.name
        return File(newname)

    def delPrefix(self, name, prefix=""):
        split = name.split(prefix)  # on veut supprimer ici le préfixe "crypt_" s'il existe.
        for i in split:
            if Path(i).suffix:
                name = i
        return name

    def addPrefix(self, name, prefix=""):
        """ cette fonction ajoute un prefixe à un nom de fichier qui a
        :param name: str
        :param prefix: str
        :return: str
        """
        newname = prefix + name
        return newname

    def extractBytesAndEncrypt(self, filename, pathfile, key):
        '''cette fonction extrait au format bytes le contenu d'un fichier ou d'un dossier source et l'encrypte, elle
        renvoie le contenu encrypté'''
        # print("\ttrying to encrypt") debuggage
        full_path = Path(pathfile).joinpath(filename)
        print(full_path)
        if Path(full_path).is_dir():
            File_list = []
            content = function_full_directory(full_path, read_bytes)
            iterateur = list(content)
            arg_list = []
            for sing_arg in iterateur:
                arg_tuple = (sing_arg, key)
                arg_list.append((sing_arg, key))

            pool = Pool(4)
            content_processing = pool.starmap(self.encryptAnyContent(), arg_list)
            File_list = content_processing
            print(File_list)
            return (File_list)
        print(f"\n\tlocation: {full_path}")
        print("\texctracting bytes")
        content = File(full_path).getContent(True)
        print("\treading bytes ok")
        encrypted_bytes = self.encryptAnyContent(content, key)
        if encrypted_bytes:
            print(encrypted_bytes)
            return encrypted_bytes
        else:
            print(f"the content of {filename} couldn't be encrypted")
            return False

    def writeBytesInFile(self, filename, content):
        file = File(filename)
        overwrite = file.writeBytes(content)
        file.closeFile()# return True si l'opération d'écriture réussie False autrement
        return overwrite

    def writeBytesInFile2(self, file: File, content):
        """ on effectue une ultime vérification avant d'écraser le fichier.
        :param file : ici, c'est la classe File qui remplace le simple nom de fichier
        :param content : en théorie ce doit être un contenu en Bytes
        :return : return True si l'opération d'écriture réussie False autrement
        """
        if file.checkOverwriteUI() == "overwrite":
            return file.writeBytes2(content)
        else:
            print("ERREUR: le fichier ne peut pas être écrasé [AlgoG.writeBytesinFile2]")
            return False

    def extractBytesAndDecrypt(self, filename, path, key):
        """ extrait le contenu de n'importe quel fichier et le decrypt. Cette fonction marche aussi si le chemin pointe
        vers un dossier.
        NB: Avec notre classe Directory la liste de chemin d'arborescence est déjà directement générée"""
        print("\ttrying to decrypt")
        full_path = Path(path).joinpath(filename)
        print(full_path)
        if Path(full_path).is_dir():
            File_list = []
            content = function_full_directory(full_path, read_bytes)
            iterateur = list(content)
            for sing_content in iterateur:
                decrypted_bytes = self.decryptAnyContent(sing_content, key)
                if decrypted_bytes:
                    File_list.append(decrypted_bytes)
                    return (File_list)
                else:
                    return False

        full_path = Path(path).joinpath(filename)
        print(f"\n\tlocation: {full_path}")
        print("\texctracting bytes")
        content = File(full_path).getContent(True)
        print(content)
        print("\treading bytes ok")
        decrypted_bytes = self.decryptAnyContent(content, key)
        if decrypted_bytes:
            print(f"\t{decrypted_bytes}")
            return decrypted_bytes
        else:
            print("impossible de décrypter le contenu. vérifier que la clé convient ou que le fichier a bien du contenu"
                  "crypé par une clef Fernet")
            return False

    def writeDecryptedContentInFile(self, filename, content):
        '''Ecrire un contenu de fichier decrypté dans un fichier au même nom que le fichier d'origine avant cryptage '''
        path = Path(filename)
        parent = path.parent
        filename = self.delPrefix(filename, "crypt_")  # suppression du préfixe "crypt_"
        if os.path.isfile(
                filename):  # si le fichier existe déjà sous ce nom là on vérifie qu'on a la droit de l'écraser
            overwrite = self.writeBytesInFile(filename, content)
            if not overwrite:  # si on n'a pas le droit d'écraser le fichier on le renomme en ajoutant un préfixe
                filename = self.addPrefix(filename,
                                          "Decrypt_")  # le fichier 'crypt_name' devient 'Decrypt_name' pour éviter
                # d'écraser un fichier existant"...
                self.writeBytesInFile(filename, content)
        else:
            self.writeBytesInFile(filename, content)

    def writeEncryptedContentInFile(self, filename, content):
        """ On ajoute une extension .crypt au fichier sans extension pour simplifier les opérations de décryptage"""
        if not File(filename).suffix:
            filename = add_extension(filename, ".crypt")
        newname = self.addPrefix(filename, "crypt_")
        self.writeBytesInFile(newname, content)

    def addPrefixAndExtension(self, file: File):
        """ On ajoute une extension .crypt aux fichiers sans extension pour simplifier les opérations de décryptage
        et on ajoute un préfixe crypt_ au nom de fichier original enfin on invoque la fonction d'écriture spéciale"""
        if not file.suffix:
            file.name = add_extension(file.name, ".crypt")
        newname = self.addPrefix(file.name, "crypt_")  # on ajoute le préfixe
        newpath = file.path.parent / newname  # on fait bien attention de reconfigurer le chemin complet vers le fichier
        newfile = File(newpath)  # on instancie la classe File à partir de ce chemin complet. Il n'est pas impossible
        # qu'un fichier porte déjà ce nom-là il ne s'agit pas forcément d'un fichier vide et il faudra le vérifier.
        return newfile

    def decryptFileOperation(self, filename, path, key):
        """L'opération de décryptage d'un fichier simple. On commence par extraire le contenu et à le decrypter
        puis on écrit le contenu dans un noouveau fichier
        ATTENTION : la fonction d'écriture est très spécifique et permet de renommer automatiquement les fichiers """
        try:
            content = self.extractBytesAndDecrypt(filename, path, key)
            if content:
                self.writeDecryptedContentInFile(filename, content)
                return True
            else:
                return False
        except:
            print(f"impossible de décrypter le fichier {filename}")
            return False

    def decryptFileOperation2(self, file: File, decryptfile: File, key):
        """L'opération de décryptage d'un fichier simple. On commence par extraire le contenu et à le decrypter
        puis on écrit le contenu dans un noouveau fichier
        ATTENTION : la fonction d'écriture est très spécifique et permet de renommer automatiquement les fichiers """
        content = self.extractBytesAndDecrypt(file.name, file.path.parent, key)
        if content:
            if decryptfile.checkOverwriteUI() == "overwrite":
                self.writeBytesInFile2(decryptfile, content)
                if file.name != decryptfile.name:
                    self.removeFile(file)
            elif decryptfile.checkOverwriteUI() == "ask overwrite":
                print("can't overwrite the file: AlgoG DecryptFileOperation2")
                return "ask overwrite"
        else:
            print("ERREUR AlgoG.decryptFileOpération2:"
                  "\néchec du décryptage dû à une mauvaise clé ou à un contenu de fichier vide ou non crypté")

    def decryptOneFileAndRemove(self, filename, path, key):
        """ATTENTION CETTE FONCTION DOIT ETRE PRESERVEE ET NE FAIT PAS DOUBLET AVEC LA PRECEDENTE.
        Elle permet de supprimer le fichier source "crypt_name" après décryptage, mais à cause des accès OS
        on ne peut pas l'utiliser directement dans le décryptage des fichiers d'un dossier, il faut les supprimer plus
        tard."""
        self.decryptFileOperation(filename, path, key)
        os.remove(filename)

    def decryptDirectoryOperation(self, fileList, key):
        """Décryptage des fichiers d'un dossier avec toute son arborescence :
        opération en deux temps : 1) on applique à chaque élément de la liste la fonction decryptFile et 2) on supprime
        les fichiers les uns après les autres.
        NB : À cause des accès OS à la liste de fichiers on ne peut pas utiliser directement la fonction pcdte."""
        os.system('COLOR 02')
        for i in fileList:
            try:
                if self.decryptFileOperation(i.name, i.path.parent, key):
                    if "crypt_" in i.name: # si le fichier crypté avait un préfixe "crypt_" on supprime ce fichier
                        # sinon on ne fait rien.
                        self.removeFile(i)  # ou bien i.deleteFile() directement TODO: à essayer
            except:
                print(f"impossible de décrypter le fichier {i.name}: see its content:\n {i.getContent(True)}")

    def decryptDirectoryOperation2(self, fileList, key):
        """Décryptage des fichiers d'un dossier avec toute son arborescence :
        opération en deux temps : 1) on applique à chaque élément de la liste la fonction decryptFile et 2) on supprime
        les fichiers les uns après les autres.
        NB : À cause des accès OS à la liste de fichiers on ne peut pas utiliser directement la fonction pcdte."""
        for i in fileList:
            try:
                if self.decryptFileOperation2(i.name, i.path.parent, key) != "ask overwrite":
                    if "crypt_" in i.name: # si le fichier crypté avait un préfixe "crypt_" on supprime ce fichier
                        # sinon on ne fait rien.
                        self.removeFile(i)  # ou bien i.deleteFile() directement TODO: à essayer
            except:
                print(f"impossible de décrypter le fichier {i.name}: see its content:\n {i.getContent(True)}")


    def cryptOneFileAndRemove(self, filename, path, key):
        """Utiliser la classe File plutôt"""
        # TODO: implémenter une option de choix sur la suppression du fichier source
        self.cryptFileOperation(filename, path, key)
        os.remove(filename)

    def cryptFileOperation(self, filename, path, key):
        """Utiliser la classe File plutôt"""
        content = self.extractBytesAndEncrypt(filename, path, key)
        self.writeEncryptedContentInFile(filename, content)

    def cryptFileOperation2(self, file: File, cryptfile: File, key):
        """ Essai d'utilisation de la classe file"""
        filename = file.name
        parentpath = file.path.parent
        try:
            content = self.extractBytesAndEncrypt(filename, parentpath, key)
            if content:
                if cryptfile.checkOverwriteUI() == "overwrite":
                    self.writeBytesInFile2(cryptfile, content)
                    self.removeFile(file)
                    return True
                elif cryptfile.checkOverwriteUI() == "ask overwrite":
                    print("can't overwrite the file: AlgoG cryptFileOperation2")
                    return False
            else:
                return False
        except:
            return False

    def cryptDirectoryOperation(self, file_list, key):
        """ATTENTION: On ne peut pas utiliser directement la fonction cryptOneFileAndRemove à cause des accès OS à nos
        fichiers."""
        os.system('COLOR 02')
        for i in file_list:
            self.cryptFileOperation(i.name, i.path.parent, key)
            self.removeFile(i)  # ou bien directement i.deleteFile()

    def cryptDirectoryOperation2(self, file_list, key):
        """ATTENTION: On ne peut pas utiliser directement la fonction cryptOneFileAndRemove à cause des accès OS à nos
        fichiers."""
        os.system('COLOR 02')
        for i in file_list:
            cryptfile = self.addPrefixAndExtension(i)
            self.cryptFileOperation2(i, cryptfile, key)
            self.removeFile(i)  # ou bien directement i.deleteFile()

    def removeFile(self, file: File):
        """Inutile si on appelle directement la méthode sur l'objet de la classe File."""
        try:
            file.deleteFile()
        except:
            if file:
                print(f"impossible de supprimer le fichier {file.name} au chemin {file.path}")
            else:
                print("impossible de supprimer le fichier: file is probably NONE")

    def typeAndRecord(self, firstLine, file):
        """cette méthode est assez générale et permet de donner un input() utilisateur pour entrer du texte à répétition
        en validant le texte par la touche 'enter', on sort de la boucle en envoyant une ligne vie.
        TODO: en faire une classe fille de Choix incluant divers paramètres"""
        l = []
        l = [firstLine]
        while True:
            line = input("\n\tnewline:")
            line = line
            l.append(line)
            if line == "":
                print("end of the message")
                break
        for i in l:
            file.appendContent(i)
        content = file.getContent()
        return content


    def play_sound(self,sound_file):
        if os.name == "nt":
            from winsound import PlaySound
            source_dir = Path(self.app_path)
            path = Path(sound_file)
            sound_file = path.name
            os.chdir(path.parent)
            PlaySound(sound=sound_file, flags=winsound.SND_FILENAME)
            os.chdir(source_dir)
            print(os.getcwd())
        else:
            from kivy.core.audio import SoundLoader
            sound = SoundLoader.load(sound_file)
            if sound:
                print("Sound found at %s" % sound.source)
                print("Sound is %.3f seconds" % sound.length)
                sound.play()

    
    def presentation2(self):
        os.system('COLOR 02')
        if os.name == 'nt':
            args = [f"{self.app_path}\\audio\\menu.wav"]
        else:
            args = [f"{self.app_path}/audio/menu.wav"]
        playsound = threading.Thread(target=self.play_sound, args=args)
        playsound.start()
        rand = random.Random()
        try:
            a = 11111111111111111111111111111111 # we want a certain number of power of ten we want 32 numbers in a row
            b = 9 * a # since we will set an intervall in which random numbers are selected we want the same number of
            # power of ten to have a clean columns of numbers effect, so b is the max number to set the largest
            # intervall to choose a random number with randrange
            r = rand.randrange  # we just take the function without any value. Args are two integers to set an intervall
            for i in range(1700):
                print(r(a, b), r(a, b), r(a, b), r(a, b), r(a, b))
                time.sleep(0.01)
            os.chdir(f"{self.app_path}")
            for line in open('Readme.txt', 'r').read().split("\n"):
                print(line)
                # Les lignes suivantes permettent d'afficher caractère par caractère la ligne en question mais
                # la commande print() de windows n'accepte pas l'affichage sur une même ligne de caractère pris 1 par 1
                # si bien que rien ne s'affiche tant que l'itération n'est pas terminé et alors la ligne complète
                # apparaît et notre effet est gâché. Pycharm rend bien cet effet.
                # if not line == "The Matrix has you ...":
                #     print(line)
                # else:
                #     for i in line:
                #         print(i, end="") ceci permet d'imprimer sur une même ligne tous les caractères un par un
                #         time.sleep(rand.ran()) ceci permet de simuler un temps de frappe aléatoire.
                #     time.sleep(0.5)

                time.sleep(0.05)

        except:
            print("Exception: could not find the presentation File")
            time.sleep(1)
            print("\n\n\tCrypto v.1.0: This is a simple program to encrypt and decrypt a text file."
                  "\n\tby Fr. Raphael Boralevi")


if __name__ == "__main__":
    algo = AlgoG().presentation2()
