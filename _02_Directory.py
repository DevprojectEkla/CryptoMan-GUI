import os
from pathlib import Path
from _01_general import tree_list
from _02_File import File

"encore en CHANTIER"


class Directory(object):
    """ Cette classe permet de récupérer toutes les informations utiles sur un dossier et de le manipuler comme un
    objet à part entière. """

    def __init__(self, pathToDir):
        self.path = pathToDir
        self.name = ""
        self.dir = None
        self.content = None
        self.parent = ""
        self.treeFileList = []
        self.treeSubdirList = []  # pas utilisé
        self.treeNameList = []
        self.newDir()

    def newDir(self):
        """Permet d'initialiser les différentes variables de la Classe. Si le dossier existe on initialise toutes nos
        variables directement, sinon on crée un dossier vide à partir du chemin indiqué"""
        self.path = Path(self.path)
        self.name = self.path.name
        if str(self.path) == self.name:
            self.path = Path(os.getcwd()) / self.name
        self.parent = self.path.parent
        if not self.path.is_dir():
            self.path.mkdir()
        else:
            print(f" Directory: {self.path}: already exists, retrieving tree directory")
            self.mkTreeList()
            # self.__setattr__('treeFile',p_tree[0])
            # self.__setattr__('treeNameList',p_tree[1])
            # self.__setattr__('treeSubDir',p_tree[2])

        return self

        # content = File.getContent(self.path)
        # File.__setattr__(self,'content',content)

    def tree_list(self, list_path_to_file=[], list_name=[]):
        """ATTENTION : Les paramètres de cette fonction sont bien ceux-là. Il ne faut pas suivre la correction de
        Pycharm et il faut bien mettre des listes vides en paramètre, car
        la fonction est récursive sur elle-même. Les listes que nous voulons ne doivent donc pas être mise = [] à chaque
        reprise. Cette fonction renvoie la liste des chemins de fichiers contenus dans un dossier et tous ses
        sous-dossiers ainsi que la liste des purs noms de fichier."""
        iterateur = Path(self.path).iterdir()
        for subchild in iterateur:
            if Path(subchild).is_dir():
                # Cette récursivité de la fonction sur elle-même est la clé de l'algo, mais surtout la manière dont
                # on passe les listes en paramètre. Ici elles ne sont plus vides. Elles sont remplies dès que
                # l'énumération rencontre un fichier, notez bien que l'on ne récupère pas les valeurs que retourne
                # tree_list à l'intérieur de l'algo. Elle est simplement exécutée pour remplir effectivement les listes.
                # Cela est équivalent à une méthode sur une classe.
                tree_list(subchild, list_path_to_file, list_name)
            elif Path(subchild).is_file():
                # print(Path(subchild))
                list_path_to_file.append(Path(subchild))
                list_name.append(Path(subchild).name)
            else:
                print("fichier non reconnu")
            # print(List_Name)
            # print(List_path_to_file)
        return [list_path_to_file, list_name]

    def mkTreeList(self):
        """ Attention : le recours à l'algo tree_list() en statique permet de passer cette méthode sans paramètre."""
        self.treeFileList = []
        self.treeNameList = []
        treeLists = self.tree_list(list_path_to_file=[], list_name=[])
        filePathList = treeLists[0]
        # nameFileList = treeLists[1]
        for i in filePathList:
            file = File(self.path.parent / i)
            self.treeFileList.append(file)
            self.treeNameList.append(file.name)
            # self.__setattr__('treeFileList',treeFileList)
            # self.__setattr__('treeNameList',treeNameList)
            # print(self.listNameofFiles)
            # print(self.tree)

    def copyTree(self):
        """À faire une fonction qui crée un dossier qui copie l'arborescence de la classe au nouvel emplacement path"""
        if self.treeSubdirList:
            for i in list(self.treeFileList):
                i.mkdir()
        pass

    def function_full_directory(self, function):
        """ Applique une fonction au dossier entier, peut-être pas utile """
        iterateur = list(self.treeFileList)
        List_result = []
        for file in iterateur:
            sing_result = function(file)
            List_result.append(sing_result)
        return List_result


if __name__ == "__main__":
    Mydir = Directory('Lib')
    print(Mydir.name, Mydir.treeFileList)
