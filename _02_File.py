import os
import time
from pathlib import Path
import subprocess
from _02_Classes import Choix


class File(object):

    def __init__(self, path_to_file='tempFile'):
        self.path = path_to_file
        self.name = ""
        self.file = None
        self.content = None
        self.suffix = ""
        self.lines = []
        self.overwrite = None
        self.f_exists = None
        self.stem = None
        self.mode = None  # TODO: intégrer un flag 'mode' pour savoir en quel mode le fichier est ouvert

        self.initFile()  # initialisation des variables

    def initFile(self):
        '''crée un nouveau fichier OU ouvre un fichier existant en mode append
         renvoie dans les deux cas un objet fichier'''
        self.path = Path(self.path)
        parent = self.path.parent

        if Path(parent).is_dir():
            os.chdir(parent)
        name = self.path.name
        suffix = self.path.suffix
        stem = self.path.stem
        if not os.path.isfile(self.path):
            self.file = open(name, 'wb')
        elif os.path.isdir(self.path):
            print("EROOR the path doesn't point to a file but to directory")
            self.file = None
        else:
            print(f" file: {self.path}: already exists, opening file in append mode")
            self.file = open(name, 'rb')
        self.__setattr__('f_exists', True)
        self.__setattr__('name', name)
        self.__setattr__('stem', stem)
        self.__setattr__('suffix', suffix)
        if self.suffix == ".txt":
            lines = self.createListFromFile()
            self.__setattr__('lines', lines)
        # content = File.getContent(self.path)
        # File.__setattr__(self,'content',content)
        return self.file

    def instanceFile(self, path):
        return File(path)


    def CheckNewFile(self):
        """Ici on veut verifier si l'on a oui ou non créer un nouveau fichier """
        if self.f_exists:
            return False
        else:
            return True

    def majFile(self):
        self.closeFile()
        self.file = self.initFile()

    def checkOverwriteUI(self):
        """ Fonction pour l'interfaçage entre une demande utilisateur et l'opération d'écriture dans un fichier existant
        il faut que la fonction d'interface utilisateur (GUI ou pas) prévoit une condition
        if checkoverwrite == 'ask overwrite' """
        if self.overwrite:
            return "overwrite"
        else:
            if self.getContent(True):
                return "ask overwrite"
            else:
                self.__setattr__('overwrite', True)
                return "overwrite"

    def overwriteMode(self):
        os.chdir(self.path)
        return open(self.path, "w")

    def readMode(self):
        return open(self.path, 'r')

    def readBytesMode(self):
        return open(self.path, 'rb')

    def appendMode(self):
        return open(self.path, 'a')

    def readWriteMode(self):
        return open(self.path, 'r+')

    def confirmationOverwrite(self):
        '''Demande de confirmation avant d'écraser un fichier existant.Si getContent renvoie False on estime que
        le fichier est vide et on ne demande pas de confirmation. Attention, l'instanciation File crée un fichier vide
        il est donc nécessaire de passer par cette condition plutot que par os.path.isfile'''
        if not self.overwrite:
            if self.getContent(True):
                confirmer = Choix("voulez-vous écraser le fichier existant?", prompt="#ConfirmerOVW>", check=True)
                confirmer = confirmer.boucleDeChoix()
                if confirmer:
                    self.__setattr__('overwrite', True)
                    return True
                else:
                    self.__setattr__('overwrite', False)
                    return False
            else:
                return True
        else:
            return True

    def confirmationOverwriteGUI(self, f_confirmation=False):
        """VERSION GUI: demande de confirmation avant d'écraser un fichier existant.Si getContent renvoie False on estime que
        le fichier est vide et on ne demande pas de confirmation. Attention, l'instanciation File crée un fichier vide
        il est donc nécessaire de passer par cette condition plutot que par os.path.isfile"""
        # TODO: Cette version GUI n'est pas encore prête. Il faut supprimmer la demande d'input à cet endroit.
        if not self.overwrite:
            if self.getContent(True):
                if f_confirmation:
                    self.__setattr__('overwrite', True)
                    return True
                else:
                    self.__setattr__('overwrite', False)
                    return False
            else:
                return True
        else:
            return True

    def writeBytesMode(self):
        file = open(self.path, 'wb')
        return file

    def writeBytes(self, content):
        """fonction pour écrire en bytes dans un fichier avec demande de confitmation avant d'écraser un fichier
         existant toutefois si la fonction getcontent(True) ne renvoie rien le fichier est considéré comme vide et le
         fichier est écrasé sans demande de confiramation"""
        confirmation = self.confirmationOverwrite()
        if confirmation:
            self.writeBytesMode().write(content)
            print(f"{self.name} has been overwrite.")
            return True
        else:
            print(f"{self.name} has NOT been overwrite.")
            return False

    def writeBytes2(self, content):
        """ATTENTION: Nouvelle version qui suppose la demande de confirmation "écraser fichier?" déjà effectuée
        par ailleurs"""
        try:
            self.writeBytesMode().write(content)
            print(f"{self.name} has been overwrite.")
            self.closeFile()
            return True
        except:
            print(f"ERROR in File.writeBytes method: {self.name} has NOT been overwrite.")
            return False

    def writeBytesGUI(self, content):
        """VERSION GUI:fonction pour écrire en bytes dans un fichier avec demande de confitmation avant d'écraser un fichier
         existant toutefois si la fonction getcontent(True) ne renvoie rien le fichier est considéré comme vide et le
         fichier est écrasé sans demande de confiramation"""
        confirmation = self.confirmationOverwriteGUI()
        if confirmation:
            self.writeBytesMode().write(content)
            print(f"{self.name} has been overwrite.")
            return True
        else:
            print(f"{self.name} has NOT been overwrite.")
            return False

    def getContent(self, bytes=False):
        '''ATTENTION: pour récupérer un contenu de fichier en Bytes il faut spécifier getcontent(bytes=True).
        Par défaut, on considère des manipulations de fichiers .txt mais pour des opérations plus lourdes il faut
        utiliser des bytes.'''
        if bytes:
            content = self.readBytesMode().read()
        else:
            content = self.readMode().read()
        return content

    def appendContent(self, content):
        file = self.appendMode()
        file.write(f"\n{content}")
        file.close()

    def formatCcontent(self):
        if isinstance(self.content, str):
            return self.content
        else:
            self.content = str(self.content)
            return self.content

    def createListFromFile(self):
        '''crée la liste des lignes d'un fichier texte.'''
        mylist = self.getContent().split('\n')
        return mylist
    ''' 
    def delLine(self, indice):
        """Algo de suppression d'une ligne dans un un fichier texte
        TODO:l'algo n'est pas encore fait c'est un copier coller de la fonction d'Annuaire"""

        self.file.close()
        templist = self.getContent().split("\n")
        indiceList = chercherIndiceSansChar(templist, "")
        indice_entry = listIndice(self.entry)
        if indiceList != indice_entry:
            newliste = []
            for i in indiceList:
                newliste.append(self.entry[i])
            self.__setattr__('entry', newliste)
            self.file.close()
            with overwrite_mode(self.path) as myfile:
                for i in self.entry:
                    if indice(i, self.entry) != 0:
                        myfile.write(f"\n{i}")
                    else:
                        myfile.write(
                            i)  # le premier élément de la liste ne doit pas être écrit avec un saut de ligne au début
                myfile.close()
            self.ouvrirAnnuaire()
        else:
            pass '''

    def openInNotepad(self):
        """Pour l'instant cela ne fonctionne pas, le contenu du fichier qui s'ouvre n'est pas à jour"""

        arg = self.path.split()  # la classe Popen veut des arguments sous forme de liste
        subprocess.Popen(args=arg, executable='c:\\windows\\notepad.exe')

    def closeFile(self):
        self.file.close()

    def deleteFile(self):
        self.closeFile()
        os.remove(self.path)

    def check_extension(self, ext):
        if self.suffix == ext:
            return True
        else:
            print(f"\n\tmake sure you chose the good extension for your file:"
                  f"\n\tRequired: {ext} but {self.suffix} was given")
            return False

    def changeStem(self, newstem):
        self.__setattr__('stem', newstem)
        return newstem

    def makeNameFromStemAndExt(self):
        stem = self.stem
        ext = self.suffix
        newname = stem + ext
        self.__setattr__('name', newname)
        return newname

    def instanceFileWithNewStem(self, stem):
        self.changeStem(stem)
        newname = self.makeNameFromStemAndExt()
        return File(newname)

    def renameFile(self, newname):
        return self.instanceFile(newname)

    def copyPasteFile(self, t_directory, overwrite=False):
        """copie le contenu d'un fichier dans un autre fichier de même nom. Si le fichier existe on demande confirmation
        pour l'écraser (overwrite= False),
        on peut passer outre à la demande de confirmation en mettant le paramètre sur True.
        ATTENTION: le nom de fichier d'origine dont la classe est instancié et sur laquelle on appelle cette méthode
        doit avoir été instancié par un chemin complet et non par le nom du fichier seulement.
        TODO: si la réponse à ovw est négative changer automatiquement le nom en name-copie.ext
        """
        self.content = self.getContent(True)
        t_directory = Path(t_directory)
        os.chdir(t_directory)
        t_file = self.instanceFile(self.name)  # le nouveau fichier va recevoir le même nom que le fichier source
        if overwrite:
            t_file.__setattr__('overwrite', True)
        result = t_file.writeBytes(self.content)
        if not result:
            copy = self.instanceFileWithNewStem(self.stem + "-copie")
            copy.overwrite = True
            copy.writeBytes(self.content)
        return t_file  # TODO: on pourrait imaginer une demande de renommer le fichier automatiquement
        # name-copie.ext.
        # on retourne un tuple car on veut pouvoir accéder à ces variables, on

    def moveFile(self, t_directory, overwrite=False, delete=True):
        """c'est la même fonction que précédemment mais on supprime le fichier dans le dossier source
        ATTENTION: il faut garder un oeil sur le CWD dont on change en invoquant copyPasteFile(), là encore le chemin
        pour l'instanciation de la classe sur laquelle on appelle cette méthode devra être un chemin complet."""
        myfile = self.copyPasteFile(t_directory, overwrite)
        if myfile.getContent(True) == self.content:  # ici on vérifie que le fichier copié a bien le même contenu
            # que le fichier source
            if delete:
                self.deleteFile()
                print(f"le fichier a bien été déplacé vers {t_directory}")
            else:
                print("copie réussie: ATTENTION: le fichier n'a pas pu être supprimé du dossier source")
            return myfile
        else:
            print("le contenu du fichier n'a pas pu être copié")
            return False


if __name__ == "__main__":
    file = File('C:\\Users\\boralevi\\PycharmProjects\\CryptoOO\\annuaire.docx')
    file.closeFile()
    input()
    file.copyPasteFile("C:\\Users\\boralevi\\PycharmProjects\\CryptoOO")
    file.moveFile("C:\\Users\\boralevi\\PycharmProjects\\CryptoOO\\Scripts")
    file.closeFile()
    print(file.stem)
