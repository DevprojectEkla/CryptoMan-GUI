import os
from pathlib import Path
#import base64 résidu d'un code antérieur en vu d'effectuer un test sur une clé de cryptage.
from cryptography.fernet import Fernet

from _02_File import File


class Key(File):
    '''cette classe hérite de la Classe fichier qui permet de faire tous les accès en lecture/écriture,
    l'instanciation ouvre (ou crée s'il n'existe pas) un fichier au chemin spécifié, par défaut: secret.key'''

    def __init__(self, path="secret.key"):
        super(Key, self).__init__(path)
        self.key = self.getContent(True)
        self.f_overwrite = False

        self.initVariables()

    def initVariables(self):
        self.path = Path(os.getcwd())/Path(self.path)

    def generateKey(self):
        '''génère une clé à l'aide du module Fernet
        cette fonction ne permet pas de conserver la clé dans le fichier mais seulement dans l'objet Key'''
        key = Fernet.generate_key()
        self.__setattr__('key', key)
        return key

    def initFlagOverWrite(self):
        self.f_overwrite = True

    def tryOverWrite(self):
        ''' Ici on veut pouvoir faire un essai de réécriture en invoquant la méthode overwrite avec le bon drapeau,
        normalement il n'y a pas d'échec possible à moins que le fichier soit inaccessible en réécriture'''
        try:
            self.initFlagOverWrite()
            newKey = self.overWriteKey()
            print(f"the preexisting {self.name} file as been replaced")
            return newKey
        except:
            print(f"the preexisting  {self.name} file has been preserved")
            return False

    def initNewKeyFile(self):
        '''Génère une clé et l'écrit dans le fichier en écrasant le contenu précédent
         l'opération de réécriture se fait sans essai et peut donc faire échouer le programme.'''
        self.initFlagOverWrite()
        print("initNewKeyFile:launching overWriteKey in _02_KeyFile.py")
        self.overWriteKey()

    def selectOtherKeyFile(self, newpath):
        '''Permet la réinstanciation de l'objet de la classe à partir d'un nouveau chemin de fichier, l'objet précédent
        est écrasé à son emplacement mémoire (mais pas le fichier réel correspondant)'''
        self.path = newpath
        if os.path.isfile(newpath):
            return (self.__init__(newpath))
        else:
            print("\n\tPlease make sure the other key file you want to use is in the directory and try again.")
            return False

    def checkFernet(self):
        '''Test d'une clé potentielle avant utilisation, si la clé est corrompue le test échoue ici et renvoie False'''
        try:
            print(self.key)
            key = Fernet(self.key)
            test = key.encrypt('test'.encode())
            return True
        except:
            return False


    def loadKey(self):
        '''le chargement d'une clé: retourne la clé associée à l'instance de classe uniquement si celle-ci passe le
        test de cryptage Fernet'''
        if self.checkFernet():
            key = self.key
            self.__setattr__('key', key)
            return key
        else:
            return False

    def overWriteKey(self):
        '''ici on n'initialise pas le drapeau de réécriture, l'opération peut donc échouer si le fichier clé n'est pas
        prêt à être écrasé'''
        key = self.generateKey()        
        overwrite = self.f_overwrite
        if overwrite:
            self.writeBytes(key)
            self.__setattr__('key', key)
            print(f"\n\tThis is the secret key:\n\t\t{key}\n\tPlease make sure to save"
                  f" the auto-generated secret key file 'secret.key' in a safe directory.")
            return key
        else:
            print("choose another Key file")
            return False
            
if __name__ == "__main__":
    key = Key("test.key")
    print(key.key)
    print(key)
    key.selectOtherKeyFile('secret.key')
    print(key.getContent())
    print(key)
        
