'''ATTENTION: ce module contient deux classes: ChoixFichier et ChoixDossier. La classe Choix() dont elles héritent
se trouvent dans le module plus général _02_Classes.'''

import os.path
from pathlib import Path

from _02_Classes import *
from _02_KeyFile import Key


class ChoixFichier(Choix):
    '''cette classe hérite de la classe Choix et apporte des attributs et des méthode de vérification du choix
    propre au choix d'un fichier.
    ATTENTION: on a en général besoin de contraindre tout de suite le choix du fichier par son extension
    c'est pourquoi on l'instancie si possible avec l'extension voulue'''
    def __init__(self,ext=""):
        super(ChoixFichier,self).__init__()
        self.question = "entrez un nom de fichier:"
        self.prompt = "#ChoixFichier>"
        self.check = None
        self.print = None
        self.ext = ext
        self.suffix = ""
        self.choix = ""
        self.path = ""
        self.check_ext = None
        self.f_exists = None
            
    def pathFichier(self):
        '''initialise les variables de chemin du fichier qui peut ne pas exister et retourne le chemin voulu
        Attention: le chemin peut encore n'être que fictif (rappelons que Path est une sous-classe de PurePath
        et peut donc suivant les cas ne pas faire d'accès au disque comme ici)'''
        path = Path(self.choix)
        suffix = path.suffix
        self.__setattr__('path', path)
        self.__setattr__('suffix',suffix)
        return path

    def existence(self):
        '''Test d'existence du fichier choisi'''
        if os.path.isfile(self.choix):
            self.f_exists = True
            return True
        else:
            self.f_exists = False
            return False

    def check_extension(self):
        '''test de l'extension du fichier choisi.
        Renvoie True si l'extension choisit correspond à la contrainte donnée, False autrement.'''
        if self.pathFichier():
            if self.path.suffix == self.ext:
                self.__setattr__('check_ext',True)
                return True
            else:
                if self.ext:
                    print(f"\n\tmake sure you chose the good extension for your file:"
                          f"\n\tRequired: {self.ext} but {self.suffix} was given")
                elif self.path.name:
                    print(f"\n\tmake sure you chose the good extension for your file:"
                              f"\n\tRequired: {self.ext} but '{self.path.name}' has no extension")
                else:
                    pass
                self.__setattr__('check_ext',False)
                return False
        else:
            return False

    def initChoix(self):
        '''Boucle de choix principale:
        il y a plusieurs boucle de choix possible en fonction des contraintes sur le choix du fichier
        initChoix lance une boucle par défaut qui doit servir de boucle de base à d'autre méthode. Comme elle n'effectue
        aucune vérification mais renvoie simplement la str de l'utilisateur elle ne doit en général pas être utilisée
        directement'''
        choixUtilisateur = self.boucleDeChoix()
        self.__setattr__('choix', choixUtilisateur)
        self.pathFichier()
        if self.check_extension():
            self.__setattr__('check_ext', True)
        if self.existence():
            self.__setattr__('f_exists', True)
        return choixUtilisateur

    def validerOverwrite(self):
        '''fonction écrite pour la fonction de dessous. TODO: A essayer dans d'autre contexte'''
        self.question = 'écraser le fichier existant?'
        self.prompt = "#ATTENTION>"
        #self.check_ext = False # check_ext est un flag qui indique si l'extension à bien été vérifié.pourquoi False??
        self.check = True # attention pour rappel self.check est un attribut de Choix() et signifie "vérifier réponse"
        overwrite = self.boucleDeChoix()
        return overwrite

    def validerCreationFichier(self):
        '''boucle de choix pour contraindre un choix permettant la création d'un nouveau fichier avec un nom distinct de
        tout fichier existant dans le cwd.'''
        while not (self.check_ext == True and self.f_exists == False):
            # on entre dans la boucle et on vérifie dans quel cas on se trouve:
            # si l'extension donnée est la bonne on ne sort pas de la boucle tant que le fichier existe à moins que
            # l'utilisateur choisisse l'option overwrite.
            if self.check_ext and self.f_exist :
                print(f"This name: {self.choix} is already in use for an existing file in cwd")
                overwrite = self.validerOverwrite()
                if overwrite:
                    return self.choix
            self.initChoix()
        else:
            # si effectivement on est dans le cas où l'extension donnée est bonne et le nom de fichier n'est pas déjà
            # uilisé par un autre fichier on renvoie bien l'entrée utilisateur qui servira de nom de fichier à créer.
            return self.choix

    def validerExtension(self):
        '''Boucle de choix pour l'entrée d'un nom de fichier ou d'un chemin pointant vers un fichier existant
         avec la bonne extension
        (ATTENTION: le fichier peut ne pas exister, la vérification concerne le nom du fichier et son extension)
        Lance la boucle initChoix en forçant l'utilisateur à donner la bonne extension au nom du fichier qu'il définit
        ou au fichier existant que le programme veut le voir sélectionner'''
        while not self.check_extension():
            self.initChoix()
        else:
            return self.choix

    def validerNonExistence(self):
        '''force la sélection d'un nom de fichier qui n'est pas déjà utilisé dans le current directory'''
        choix = self.validerExtension()
        if self.f_exists:
            print("This file already exists in cwd")
            self.initChoix()
        else:
            return(choix)

    def validerExistence(self):
        '''Boucle de choix pour la sélection d'un fichier existant:
        Lance la boucle initChoix en forçant l'utilisateur à donner un chemin vers un fichier existant'''
        while not self.existence():
            if self.choix:
                print("The file doesn't exist")
            self.initChoix()
        else:
            return(self.choix)

    def validerChoix(self):
        '''Boucle de choix pour la sélection d'un fichier existant avec la bonne extension:
        ATTENTION: cela peut paraître redondant, si le fichier existe il a nécessairement une extension valide mais pas
        forcément celle voulue par le programme.'''
        self.validerExtension()
        choix = self.validerExistence()
        return choix

    def chooseOtherFile(self,path):
        '''choisir un nouveau fichier si un fichier selectionner existe déja '''
        # TODO: utiliser la fonction validerCreationFichier()
        pass

    def chooseOtherKeyFile(self):
        '''Cette méthode lance la boucle de choix sur un objet ChoixFichier en contraignant l'utilisateur à entrer une
        extension .key et à choisir un fichier existant. Mais on doit aussi vérifier que le fichier choisit contient
        bien une clé de cryptage Fernet valide. Cette méthode retourne un objet Key. En cas de clé invalide on veut
        relancer la boucle de choix de fichier.'''
        self.ext = ".key"
        self.question = "Entrez un nom de fichier .key contenant une clé valide "
        filename = self.validerChoix()  # cette méthode permet de sortir avec un fichier existant
        key = Key(filename)
        if key.checkFernet():  # on vérifie que le fichier contient une clé utilisable par Fernet
            print(f"\n\tYou extracted a key from the file {filename} this is the key you will use in this session:"
                  f"\n\n\t\t{key.key}")
            time.sleep(1)
            return key
        else:
            print("the selected .key file doesn't contain a valid key, choose another one")
            self.initChoix()
            newchoice = self.chooseOtherKeyFile() # il n'est jamais aisé de devoir réinitialiser la boucle de choix
            # TODO:trouver mieux que cette merde d'algo
            return newchoice


        # else:
        #     print("the selected .key file doesn't contain a valid key, choose another one")
        #     self.initChoix()
        #     newchoice = self.chooseOtherKeyFile()  # il n'est jamais aisé de devoir réinitialiser la boucle de choix
        #     # TODO:trouver mieux que cette merde d'algo
        #     return newchoice



class ChoixDossier(Choix):
    '''Classe initialisant Choix pour le choix spécifique d'un dossier. Elle permet d'initialiser des variables propres
    à un dossier et des méthodes particulière de contrôle selon les contraintes voulu. Dossier en arborescence, contenu
    spécifique existence TODO: Finir de créer les méthodes de cette classe et tester son fonctionnement '''
    def __init__(self):
        super(ChoixDossier,self).__init__()
        self.question = "choisissez un dossier:"
        self.prompt = "#ChoixDossier>"
        self.check = False
        self.print = False        
        self.choix = ""
        self.path = ""
        self.name = ""
        self.parent = ""
        self.f_exists = False
    
    def pathDossier(self):
        path = Path(self.choix)
        parent = path.parent
        self.__setattr__('path', path)
        self.__setattr__('parent',parent)
        return path

    def existence(self):
        if os.path.isdir(self.choix):
            return True
        else:
            return False

    def initChoix(self):

        choixUtilisateur = self.boucleDeChoix()
        self.__setattr__('choix', choixUtilisateur)
        if self.existence():
            self.__setattr__('f_exists', True)
        self.pathDossier()
        return choixUtilisateur

    def validerExistence(self):
        while not self.existence():
            if self.choix:
                print("This directory doesn't exist")
            self.initChoix()
        else:
            return(self.choix)

    def ChoixArborescence(self):
        ''' on peut vouloir demander non seulement un dossier mais une liste d'un ensemble de sous-dossiers existant ou
        non dans le but de créer ou de modifier l'arborescence d'un dossier TODO:créer cette fonction '''
        pass
        

if __name__=="__main__":


    choix = ChoixFichier('.txt')
    choix.choix = "secret.key"
    choix = choix.chooseOtherKeyFile()
    #print(choix.check_extension())
    #choix.validerNonExistence()
    # print(choix.check_ext)
    # print(choix.f_exists)


    print(choix.choix)
