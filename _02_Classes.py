import os
import sys
from pathlib import Path
import subprocess
from cryptography.fernet import Fernet
import time
import base64

'''attention la class File a migrée vers le fichier _02_File.py'''

class ExtractionDeParametres(object):
    '''Cette Classe instancie un objet dont les variables servent à initier l'extraction de parametres à partir d'une
    liste de la forme ["nom numero qualité chose","nom numéro qualité chose",...,].
    liste:liste dont on va extraire des données sous forme de parametres
    separateur: caractère qui sépare les parametres, par défaut espace " "
    nb_colonnes: nombre de colonnes que l'on souhaite extraire en fonction du nombre de paramètres extractible

    ex: ['Bob 12 brun couteau', 'John 14 chatain bilboquet', Martin 18 blond toupie'] le séparateur entre chaque
    parametre est un espace ici.
    La méthode d'extraction renvoie une liste contenant la liste de chaque parametre,
    la liste des nom ['Bob','John','Martin'], la liste de numéro [12, 14, 18], etc.
    etc.'''

    def __init__(self, liste=[], separateur=" ", nb_colonnes=2):

        self.liste = liste
        self.sep = separateur
        self.nb_col = nb_colonnes  # les boucles for partent de l'indice 0 par défaut
        self.col_liste = []
        self.createColumnList()

    def createColumnList(self):
        column_list = []
        for i in range(0, self.nb_col):
            column_list.append([])
        self.__setattr__('col_liste', column_list)

    def extractItems(self):

        for item in self.liste:
            split = item.split(self.sep)
            for i in range(0, self.nb_col):
                self.col_liste[i].append(split[i])

        return self.col_liste


class Choix(object):
    '''cette Classe permet de paramètrer une boucle de choix pour un utilisateur (fonction input améliorée),
    le paramètre 'question' est une string, par défaut demande de confirmation
    'prompt' permet de styliser la console,
    'reponse' est la liste des rep. possibles elle permetra de vérifier les entrées utilisateurs,par def. 'y' ou 'n'
    'check' active ou non la vérification des entrées,
    'print_reponse' permet d'activer l'affichage des réponses possibles.
    On amorce la boucle en appelant une des méthodes 'boucleDeChoix' ou 'splitChoix', etc. selon la nature du traitement
    voulu pour les données d'entrée utilisateur.
    NB: les méthodes renvoient un Booléen pour une question oui/non mais elle renvoie une str dans tous les autres
    cas. '''

    def __init__(self, question="êtes-vous sûr?", prompt="#>", reponse=['y', 'n'], check=True, print_reponse=False):
        self.question = question
        self.prompt = prompt
        self.reponse = reponse
        self.check = check
        self.print = print_reponse

    def __getattr__(self, item):
        return self.question, self.prompt, self.reponse, self.check

    def printReponse(self):
        if self.print:
            print(self.reponse)

    def boucleDeChoix(self):
        """ C'est la méthode de base qui amorce la boucle de choix, elle permet d'effectuer un minimum de contrôle
        sur les entrées utilisateurs, par ex: si la réponse de l'utilisateur ne correspond à rien de la liste "reponse"
        la boucle recommence (si 'check' est True) en imprimant toutes les réponses possibles, etc. """
        while True:
            print(self.question)
            Choix.printReponse(self)
            choix = input(self.prompt)
            if choix == 'exit':
                print("au revoir")
                time.sleep(1)
                sys.exit(0)
            elif choix == "cancel":
                return 'CANCEL'
            else:
                if self.check:
                    iterateur = list(self.reponse)
                    if choix in iterateur:
                        if choix == 'y':
                            return True
                        elif choix == 'n':
                            return False
                        else:
                            return choix  # cette ligne semble fautive car elle renvoit True en cas de choix
                    else:
                        print(f"please choose an answer among: {self.reponse}")
                else:
                    return choix

    def splitChoix(self, separateur=" "):
        '''cette méthode permet un traitement spécial des entrées utilisateurs par l'utilisation de la fonction split()
        dont le séparateur par défaut est un espace, elle renvoit la liste des arguments d'une chaine séparés
        par ce séparateur.'''
        while True:
            choix = self.boucleDeChoix()

            if choix:
                if isinstance(choix, list):
                    choix = choix[0]
                if separateur in choix:
                    iterateur = list(self.reponse)
                    choix = choix.split(separateur)
                    if choix[0] in iterateur and len(choix[1].lstrip().split()) == 2:
                        return choix
            else:
                print(f"all values must be chosen among: {self.reponse}")
                self.print = False

    def choix_value(self, value_type='str'):
        '''pas encore opérationnelle, on veut ici effectuer un traitement des entrées utilisateurs pour renvoyer un type
         désiré (bool, int, str, etc.)'''  # TODO finir de programmer cette fonction
        while True:
            print(self.question)
            if self.check:
                choix = input(f"choose a {value_type} type")
            else:
                choix = input(self.prompt)

            if isinstance(choix, value_type):
                return choix
            else:
                if value_type is int:
                    try:
                        int(choix)
                        print(choix)
                        return choix
                    except:
                        self.check = True

                self.check = True


class RepeatOperation(object):
    '''cette classe sert à réitérer une demande d'opération utilisateur sur une classe ou une fonction, la demande
    d'input est réitérée à chaque fois et l'utilisateur peut effectuer la même opération autant de fois qu'il le demande
    il peut interrompre la boucle de répétition à tout moment. La méthode 'boucleSimple' permet d'effectuer une boucle
    sur une fonction dataInput qui est une méthode de classe, la méthode 'loop' prend en charge des demandes d'input
    plus complexe impliquant un ou plusieurs paramètres'''

    def __init__(self, dataInput: object, mainFunction: object, param=[], special=False):
        self.input = dataInput
        self.function = mainFunction
        self.param = param
        self.special = special

    def boucleSimple(self):
        '''cette méthode doit servir quand on passe en argument dataInput une méthode sur une classe qui renvoie une
        valeur de type str utilisable telle quelle (notez les parenthèse dans self.input() où self.input est une méthode
        ou une fonction n'appelant aucun paramètre, si on veut une fonction input à laquelle on doit passer
        des arguments il faut utiliser la méthode loop '''

        while True:
            data = self.input().split()
            p_function = self.function.__defaults__
            p_number = len(p_function)

            if not data:
                print("operation canceled")
                break
            elif p_number == 1:
                self.function(data[0])
            elif p_number == 2:
                self.function(data[0], data[1])
            elif p_number == 3:
                self.function(data[0], data[1], data[2])
            else:
                print("operation canceled")
                return 0
            if not Choix("continuer cette opération?", check=True, print_reponse=True).boucleDeChoix():
                break

    def loop(self):
        while True:
            if self.special:
                self.param = special_p(special_op, self.param)
            param_number = len(self.param)
            if param_number == 1:
                data = self.input(self.param[0])
            elif param_number == 2:
                data = self.input(self.param[0], self.param[1])
            elif param_number == 3:
                data = self.input(self.param[0], self.param[1], self.param[2])
            elif param_number == 4:
                data = self.input(self.param[0], self.param[1], self.param[2], self.param[3])
            if len(self.param) > 1:
                prompt = self.param[1]
            else:
                prompt = "#>"
            '''on récupère ici le nombre de parametre de la fonction 'function' mais attention pour avoir accès au bon
            nombre de parametre et à leur type au besoin, il faut fixé des valeurs par défauts qui sont appelées par 
            la methode __defaults__, laquelle renvoie un tuple avec les valeurs par défauts'''
            if data:
                p_function = self.function.__defaults__
                p_number = len(p_function)
                if p_number == 1:
                    self.function(data[0])
                elif p_number == 2:
                    self.function(data[0], data[1])
                elif p_number == 3:
                    self.function(data[0], data[1], data[2])
            else:
                print("operation canceled")
                return 0
            if not Choix("continuer cette opération?", prompt, check=True, print_reponse=True).boucleDeChoix():
                break

if __name__ == '__main__':
    dir = Directory('prout')
    print(dir.treeDir)

    print(dir.nameList)
    print(dir.mkTreeList(dir.path)[2])
    dir.copyTree()
    # quelques exemples d'utilisation de nos classes, please uncomment les exemples pour une pleine expérience.
    # key = Key('secret.key')
    # key.generateKey()

    # print(key.path)
    #print(key.key)
    # key.overWriteKey()
    # key.selectOtherKeyFile('secret.key')
    # print(key.path)
    # print(key.key)
    # extract = ExtractionDeParametres(['Atchoum le nain jaune','José le caïd noir','Coco le oiseau bleu',
    #                                 'Jerome le mamouth gris'],nb_colonnes=4).extractItems()
    # print(extract)
'''
    try:
        print.__defaults__()
    except:
        print ("la fonction 'print' native n'a pas de parametre 'value' par défaut")
    print("il est donc nécessaire de créer une fonction personnalisée pour l'utiliser"
          " comme parametre de notre classe RepeatOp.")
    def Myprint(value=""):
        print(value)
    test = Choix('démarrer le test?',print_reponse=True).boucleDeChoix()

    if test:
        print("on utilise la fonction Myprint au lieu de print dans les parametre de la Classe ci-dessous")
        print('RepeatOperation(Choix(...).boucleDeChoix, Myprint,...).boucleSimple()')
        RepeatOperation(Choix("choisissez une entrée à afficher",
                         "#Admin>", ["Bonjour","Toto"], True, True).boucleDeChoix, Myprint).boucleSimple()
    else:
        print ("au revoir")'''