'''ce module contient des fonctions et des classes très générales '''

'importation des modules natifs usuels'
import os
import stat
import time
import sys
import subprocess
from pathlib import Path



def open_notepad(fichier:str):

    arg = fichier.split()
    subprocess.Popen(args=fichier, executable = 'c:\\windows\\notepad.exe' )

def new_file(pathfile):
    if not os.path.isfile(pathfile):
        file = open(pathfile,'w')
    else:
        print(f" file: {pathfile}: already exists, opening file in append mode")
        file = open(pathfile, 'a')
    return file

def overwrite_mode(pathfile):
    file = open(pathfile,"w")
    return file


def read_mode(pathfile):
    file = open(pathfile, 'r')
    return file


def read_write_mode(pathfile):
    file = open(pathfile, 'r+')
    return file


def append_mode(pathfile):
    file = open(pathfile,'a')
    return file


def file_content(pathfile):
    content = read_mode(pathfile).read()
    return content


def append_content(pathfile,content):
    append_mode(pathfile).write(content)


def format_content(content):
    if isinstance(content, str):
        return content
    else:
        content = str(content)
        return content


def create_list_from_file(pathfile):
    list = open(pathfile, 'r').read().split('\n')
    return list


def extract_items(list):
    ''' Cette fonction se contente d'extraire les deux premières "colonnes" d'une liste de
    paramètre (type string) séparés par des espaces.
    ex: extract_items(['dupont 18','smith 007 out'])
    renvoie: ['dupont','smith'],['18','007']
    voir la Classe ExtractionDeParametre pour une généralisation à un nombre quelconque de parametres'''

    # TODO supprimer cette fonction qui ne sert plus à rien
    colonne1 = []
    colonne2 = []
    for item in list:
        split = item.split(" ")
        element1 = split[0]
        colonne1.append(element1)
        if len(split) > 1:
            element2 = split[1]
            colonne2.append(element2)
    return colonne1, colonne2


def indice(item,list):
    n = 0
    for i in list:
        if i == item:
            break
        else:
            n+=1
    return n

def supprimerDoublons(Liste):
    '''ne marche pas encore'''
    clean = []
    for i in Liste:
        Liste.remove(i)
        if not i in Liste:
            clean.append(i)
        else:
                pass
    return clean
        

def special_p(special_op,param):
    pass

'''ATTENTION AU DOUBLONS AVEC _02_Classes'''
#TODO: supprimer ces classes après avoir vérifier la version la plus à jour.

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

    def __init__(self, liste = [], separateur = " ", nb_colonnes = 2):

        self.liste = liste
        self.sep = separateur
        self.nb_col = nb_colonnes # les boucles for partent de l'indice 0 par défaut
        self.col_liste = []
        ExtractionDeParametres.createColumnList(self)

    def createColumnList(self):
        column_list = []
        for i in range(0, self.nb_col):
            column_list.append([])
        ExtractionDeParametres.__setattr__(self,'col_liste',column_list)


    def extractItems(self):

        for item in self.liste:
            split = item.split(self.sep)
            for i in range (0, self.nb_col):
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
    NB: les méthodes renvoient un Booléen pour une question oui/non mais elle renvoie une liste dans tous les autres
    cas. Cette liste est de la forme [entrée utilisateur, itérateur des reponses possibles] '''

    def __init__(self,question="êtes-vous sûr?", prompt="#>", reponse=['y','n'], check = True,print_reponse= False):
        self.question = question
        self.prompt = prompt
        self.reponse = reponse
        self.check = check
        self.print = print_reponse


    def __getattr__(self, item):
        return self.question,self.prompt,self.reponse,self.check

    def printReponse(self):
        if self.print:
            print(self.reponse)

    
    def boucleDeChoix(self):
        ''' c'est la méthode de base qui amorce la boucle de choix, elle permet d'effectuer un minimum de contrôle
        sur les entrées utilisateurs, par ex: si la réponse de l'utilisateur ne correspond à rien de la liste "reponse"
        la boucle recommence (si 'check' est True) en imprimant toutes les réponses possibles etc. '''
        while True:
            print(self.question)
            Choix.printReponse(self)
            choix = input(self.prompt)
            if choix == 'exit':
                print("au revoir")
                time.sleep(1)
                sys.exit(0)
            elif choix == "cancel":
                return False
            else:
                if self.check:
                    iterateur = list(self.reponse)
                    if choix in iterateur:
                        if choix == 'y':
                            return True
                        elif choix == 'n':
                            return False
                        else:
                            return [choix, list(self.reponse)]
                    else:
                        print(f"please choose an answer among: {self.reponse}")
                else:
                    return [choix, list(self.reponse)]


    def splitChoix(self,separateur=" "):
        '''cette méthode permet un traitement spécial des entrées utilisateurs par l'utilisation de la fonction split()
        dont le séparateur par défaut est un espace, elle renvoit la liste des arguments d'une chaine séparés
        par ce séparateur.'''
        while True:
            choix = Choix.boucleDeChoix(self)

            if choix:
                if isinstance(choix,list):
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
         désiré (bool, int, str, etc.)'''# TODO finir de programmer cette fonction
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
    def __init__(self,dataInput:object, mainFunction:object, param = [], special = False):
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
            data = self.input()
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
            if not Choix("continuer cette opération?", prompt, check= True, print_reponse= True).boucleDeChoix():
                break


def convert_type(value, type):
    pass

def parent_path(List_path_to_file):
    ''' d'une liste de chemin pointant vers des fichiers on établit la liste des chemins parents de ces fichiers '''
    parent_list = []
    for i in List_path_to_file:

        if Path(i).suffix:  # si il y a un suffix c'est qu'il s'agit d'un chemin pointant vers un fichier,
            # on veut en récupérer le chemin parent
            subdir = Path(i).parent
            parent_list.append(subdir)
        else:  # s'il n'y a pas de suffix, il s'agit d'un dossier et on l'ajoute directement à la liste
            parent_list.append(Path(i))

    return parent_list


def add_extension(filename, suffix):
    '''Pour certains fichier qui n'ont pas d'extension et ne sont pas reconnu comme fichier par la fonction Path.is_dir
    on utilise le module stat et la constante S_ISDIR qui est manifestement plus précise pour déterminer si le terme
    sans extension est un fichier ou un dossier'''
    if (isinstance(filename,str)):
        mode = os.stat(filename).st_mode
        if not stat.S_ISDIR(mode) and not Path(filename).suffix:
            new_extension = Path(filename).with_suffix(f"{suffix}")
            new_extension = str(new_extension) # si newextension est au format Path() c'est indispensable.
            return new_extension

def del_extension(filename, suffix):
    """Pour certains fichier qui ont reçu une extension dont on veut se débarasser """
    if Path(filename).suffix == suffix:
        with_no_extension = str(Path(filename).stem)
        return with_no_extension
    else:
        return filename


def add_extension_listFiles(list_files, suffix):
    '''Pour certains fichier qui n'ont pas d'extension et ne sont pas reconnu comme fichier par la fonction Path.is_dir
    on utilise le module stat et la constante S_ISDIR qui est manifestement plus précise pour déterminer si le terme
    sans extension est un fichier ou un dossier'''
    if (isinstance(list_files,str)):
        mode = os.stat(list_files).st_mode
        if not stat.S_ISDIR(mode) and not Path(list_files).suffix:
            new_extension = Path(list_files).with_suffix(f"{suffix}")

    new_list = []

    for i in list_files:
        mode = os.stat(i).st_mode
        if not stat.S_ISDIR(mode) and not Path(i).suffix:
            new_extension = Path(i).with_suffix(f"{suffix}")
            new_list.append(new_extension)
        else:
            new_list.append(i)
    return new_list


def compare_path(path1, path2):
    ''' de deux chemins emboités renvoie un sous-chemin intermédiaire qui pointe vers le fichier
      ex: path1 = c:/users/boralevi/test et path2 = c:/users/boralevi/test/image/image1.png
    la fonction renvoie path = image/image1.png '''

    Normpath1 = Path(path1)
    Normpath2 = Path(path2)
    path = ""
    list_subdir = []
    compare = True
    '''on ne veut pas que la fonction tienne compte de l'ordre des arguments '''
    if Normpath1.is_relative_to(Normpath2):
        op_path1 = Normpath1
        op_path2 = Normpath2

    elif Normpath2.is_relative_to(Normpath1):
        op_path1 = Normpath2
        op_path2 = Normpath1

    else:
        compare = False
        print("\n\tthe pass are not related one to another, no common path for subdir to find")
        return (0)

    if compare:
        for i in op_path1.parts:
            if i not in op_path2.parts:
                list_subdir.append(i)
        for i in list_subdir:
            path = Path(f"{path}/{i}")

        return (path)


def mklist_subdir(src_directory, List_fullpath_file):
    '''ici on créé la liste des sous chemins correspondant à l'arborescence que l'on veut copier, le premier argument
    est un chemin qui pointe vers le dossier duquel on veut imiter l'arborescence, le second argument est la liste des
    vrais chemins de fichiers tiré de ce dossier source et de ses sous-dossiers,
    le résultat doit renvoyer les chemins d'arborescence intermédiaire qui partent du dossier source
    (donc non plus c:/.../dossier source/fichier.txt mais bien dossier_source/fichier.txt) ces chemins pointent vers
    le fichier contenu dans le ou les sous dossiers ex: source/sous-dossier1/ss-dossier2/fichier.txt'''
    list_subdir = []
    for i in List_fullpath_file:
        path_subdir = compare_path(src_directory, i)
        list_subdir.append(path_subdir)

    return (list_subdir)


def mklist_new_tree(target_directory, list_subdir):
    ''' etant donné le chemin d'un dossier target ou l'on veut copier des fichier venant d'un autre dossier dont on
    veut copier l'arborescence on importe la liste des sous chemins d'arborescence du dossier source et on concatène
    chaque sous chemin avec le chemin target. On renvoit ensuite la liste
    des nouveaux chemins de destinations.NB: ces chemins sont encore artificiels, sans existence concrète  '''
    list_new_tree = []
    if target_directory.is_dir():
        p = Path(target_directory)
        if isinstance(list_subdir, list):
            for i in list_subdir:
                newpath = os.path.normpath(f"{p}/{i}")
                list_new_tree.append(newpath)
        else:
            print("make sure to take a valid list of arguments")
    else:
        print("\n\tmake sure to select a valid target directory and a valid list")

    return list_new_tree


def tree_list(directory, List_path_to_file=[], List_Name=[]):
    '''cette fonction renvoie la liste des chemins de fichiers contenus dans un dossier et tous ses sous-dossiers
    ainsi que la liste des purs noms de fichier'''
    iterateur = Path(directory).iterdir()
    for subchild in iterateur:
        if Path(subchild).is_dir():
            tree_list(subchild, List_path_to_file, List_Name)
        elif Path(subchild).is_file():
            # print(Path(subchild))
            List_path_to_file.append(Path(subchild))
            List_Name.append(Path(subchild).name)
        else:
            print("fichier non reconnu")
        # print(List_Name)
        # print(List_path_to_file)
    return ([List_path_to_file, List_Name])


def function_full_directory(directory, function):
    ''' applique la fonction à tous les fichiers d'un dossier et de ses sous-dossier'''
    iterateur = list(tree_list(directory, [], [])[0])
    List_result = []
    for file in iterateur:
        sing_result = function(file)
        List_result.append(sing_result)
    return List_result

def check_extension(file_name: str, ext: str):
    try:
        suffix = Path(file_name).suffix
        if suffix == ext:
            return True
        else:
            print(f"\n\tmake sure you chose the good extension for your file:"
                  f"\n\tRequired: {ext} but {suffix} was given")
            return False
    except:
        print(f"\n\tERROR: in check_extension function")
        return False

def confirmation(question: str):
    while True:
        confirm = input(f"\n\t{question}  'y' or 'n':\n\n\t#Crypto>")
        if confirm == 'y':
            test = True
            break
        elif confirm == 'n':
            test = False
            print("\n\tthe file will not be overwritten")
            break
        else:
            print("\n\tplease select 'y' or 'n':")

    return (test)

if __name__ == '__main__':
# quelques exemples d'utilisation de nos classes, please uncomment les exemples pour une pleine expérience.

    file = File('C:\\Users\\boralevi\\PycharmProjects\\Annuaire\\annuaire-Copie(2).txt')
    file.appendContent('Nouvelles infos')
    file.appendContent("super interessant !!")
    print(file.getContent())
    file.closeFile()
    file.openInNotepad()


    #extract = ExtractionDeParametres(['Atchoum le nain jaune','José le caïd noir','Coco le oiseau bleu',
     #                                 'Jerome le mamouth gris'],nb_colonnes=4).extractItems()
    #print(extract)
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
        print ("au revoir") '''
