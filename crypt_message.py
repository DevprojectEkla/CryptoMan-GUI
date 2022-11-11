import os.path
import os
import shlex
import sys
import subprocess
import time
import pathlib
import multiprocessing
from shutil import make_archive
from cryptography.fernet import Fernet

from _01_general import *
from _02_Classes import *


def try_again(abort, decrypt, key):
    ''' on veut proposer ici de relancer cryptoman, soit la fonction qui a échoué, soit en cas de succès le menu principal'''
    if abort:
        confirmation("\n\tDo you want to try again")
        if confirmation:

            if decrypt:
                print(f"\n\trestarting {function}")
                decrypt_file(key)
            else:
                encrypt_file(key)
        else:
            return False

    else:
        confirmation("\n\tVoulez-vous contiuer à utiliser les fonctions de Cryptoman")
        if confirmation:
            return True
        else:
            return False


def tree_list(directory, List_path_to_file=[], List_Name=[]):
    '''this function make a list of all the path of a directory pointing to a file
         and put them in a list as well as it store in a list all the corresponding file names'''
    from pathlib import Path
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
    iterateur = list(tree_list(directory, [], [])[0])
    List_result = []
    for file in iterateur:
        sing_result = function(file)
        List_result.append(sing_result)
    return List_result


def confirm(question: str):
    while True:
        confirm = input(f"\n\t{question} ?  'y' or 'n':\n\n\t#CryptoMail>")
        if confirm == 'y':
            modify = False
            break
        elif confirm == 'n':
            modify = True
            print("\n\tyou may change your input")
            break
        else:
            print("\n\tplease select 'y' or 'n':")

    return (modify)



def generate_key():
    """
    Generates a key and save it into a file
    """
    if os.path.isfile('secret.key'):
        key = Key('secret.key')
        print("using existing secret.key file")
    else:
        key = Key('secret.key')
        key.generateKey()

    print(
        f"\n\tThis is the secret key for your encrypted files (for this session only):\n\t\t{key.key}\n\tPlease make sure to save"
        f" the auto-generated secret key file 'secret.key' in a safe directory.")
    time.sleep(1)

    overWritekey = Choix("\n\tDo you want to:\n\n\tuse the already existing secret.key file (s),"
                         "\n\n\toverwrite it with the new printed key (ovw),\n\n\t"
                         "use another namefile.key (OF),"
                         "\n\n\tcreate another key file to use with this session (c) ?",
                         reponse=['s', 'ovw', 'OF', 'c'], prompt="#Crypto>", check=True,
                         print_reponse=True).boucleDeChoix()
    if overWritekey == 'ovw':
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
            print("the preexisting secret.key file as been replaced")
            return (key.key)
    elif overWritekey == 'OF':
        otherkeyfile = Choix(
            "\n\tPlease put the other .key file in the current directory and type here the name of the .key file"
            "\n\tor enter a full path pointing to the .key file:","#Crypto>",[],False,False ).boucleDeChoix()
        key.selectOtherKeyFile(otherkeyfile)
        print(f"\n\tYou extracted a key from the file {otherkeyfile} this is the key you will use in this session:\n\n\t\t{key.key},\n\tthe fresh generated one will"
              " no longer be in use.")
        time.sleep(1)
        if key:
            key = key.key
            return (key)
        else:
            print("not a good file")
    elif overWritekey == 'c':
        filename = Choix("\n\tchoose another file name for the secret key ('name.key'):\n\t", "Filename:").boucleDeChoix()
        check_ext = check_extension(filename,".key")
        if not check_ext:
            print("\n\tplease choose a name ending with the correct extension '.key'.")
        else:
            if not os.path.isfile(os.path.join(os.getcwd(), f"{filename}")):
                key = Key(filename)
                key.generateKey()
                print(f"\n\tYou created a key and saved it in the file: {filename}.\n"
                          "this is the key you will use"
                          f" in this session:\n\n\t\t{key}.\n\t")
                return (key)
            else:
                print("\n\tthis name is already in use for another key file\n"""
                      "\tplease choose another name.")
    elif overWritekey == 's':
        print(
            f"\n\tthis is the current key you will use in this session: {key.key},\n\t the fresh generated one will"
            " no longer be in use.")
        time.sleep(1)
        return (key)

    return (key)


def load_key(key_file):
    """
    Loads the key named `secret.key` from the current directory.
    """
    return open(f"{key_file}", "rb").read()


def encrypt_message(message, key):
    """
    Encrypts a message
    """

    if isinstance(message, str):
        message = message.encode("Utf8")
    f = Fernet(key)
    encrypted_message = f.encrypt(message)
    return (encrypted_message)


def encrypt_any_content(content, key):
    """
    Encrypts any type of content
    """

    if isinstance(content, str):
        content = content.encode("Utf8")
    f = Fernet(key)
    encrypted_content = f.encrypt(content)
    return (encrypted_content)


def decrypt_message(encrypted_message, key):
    check = isinstance(encrypted_message, str)
    if check:
        encrypted_message = encrypted_message.encode()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    # the decrypt message is a string
    return (decrypted_message)


def decrypt_any_content(content, key):
    """
    decrypts bytes
    """
    if isinstance(content, str):
        content = content.encode("Utf8")
    f = Fernet(key)
    decrypted_content = f.decrypt(content)
    return (decrypted_content)


def extension_file(file: str):
    if os.path.isfile(file):

        extension = pathlib.Path(file).suffix
        return (extension)
    else:
        print(f"\n\tcannot find the file:{file}, no extension retreive")


def check_extension(file_name: str, ext: str):
    try:
        suffix = pathlib.Path(file_name).suffix
        if suffix == ext:
            return True
        else:
            print(f"\n\tmake sure you chose the good extension for your file:"
                  f"\n\tRequired: {ext} but {suffix} was given")
            return False
    except:
        print(f"\n\tERROR: in check_extension function")
        return False


def check_txtFile(file: str):
    if os.path.isfile(file):

        try:

            extension = pathlib.Path(file).suffix
            if extension == ".txt":
                print("the file is a .txt")
                return True
            else:

                return False
        except:
            print("the name of the file should contain the extension '.txt'")
            return False
    else:
        print("\n\tthe name you entered doesn't point to an existing file")
        return (False)


def goodbye():
    try:
        print(open("goodbye.txt", "r").read())
    except:
        print("\n\t could not open file Goodbye.txt")
        print("\n\tGoodbye, thanks for using Cryptoman hope you enjoyed it.")


def open_file(file_name, my_path):
    norm_path = os.path.normpath(my_path)
    if os.path.isfile(file_name):
        file_name = os.path.basename(file_name)

    complete_path = os.path.join(norm_path, file_name)
    print("complete path ok")

    if check_txtFile:
        New_file = open(complete_path, "r")
        content = New_file.read()
    else:
        print("chk bytes ok")
        New_file = open(complete_path, "rb")
        content = New_file.read()
        print("reading bytes")

    return (content)


def extract_str_and_encrypt(file_name, my_path, key):
    content = open_file(file_name, my_path)
    encrypted_msg = encrypt_message(content, key)
    print(encrypted_msg)
    return (encrypted_msg)


def read_bytes(file):
    try:
        content = pathlib.Path(file).read_bytes()
    except:
        content = pathlip.Path(file).read_text()
    return (content)


def extract_bytes_and_encrypt(file_name, my_path, key):
    '''cette fonction extrait au format bytes le contenu d'un fichier ou d'un dossier source et l'encrypte, elle
    renvoie le contenu encrypté'''
    # print("\ttrying to encrypt") debuggage
    full_path = pathlib.Path(my_path).joinpath(file_name)
    print(full_path)
    if pathlib.Path(full_path).is_dir():
        File_list = []
        content = function_full_directory(full_path, read_bytes)
        iterateur = list(content)
        arg_list = []
        for sing_arg in iterateur:
            arg_tuple= (sing_arg,key)
            arg_list.append((sing_arg, key))

        pool = multiprocessing.Pool(4)
        content_processing = pool.starmap(encrypt_any_content, arg_list)
        File_list = content_processing
        print(File_list)
        return (File_list)
    print(f"\n\tlocation: {full_path}")
    print("\texctracting bytes")
    content = pathlib.Path(full_path).read_bytes()
    print("\treading bytes ok")
    encrypted_bytes = encrypt_any_content(content, key)
    print(encrypted_bytes)
    return (encrypted_bytes)


def extract_str_and_decrypt(file_name, my_path, key):
    content = open_file(file_name, my_path)
    decrypted_msg = decrypt_message(content, key)
    return (decrypted_msg)


def extract_bytes_and_decrypt(file_name, my_path, key):
    ''' works with a directory'''
    print("\ttrying to decrypt")
    full_path = pathlib.Path(my_path).joinpath(file_name)
    print(full_path)
    if pathlib.Path(full_path).is_dir():
        File_list = []
        content = function_full_directory(full_path, read_bytes)
        iterateur = list(content)

        for sing_content in iterateur:
            decrypted_bytes = decrypt_any_content(sing_content, key)
            File_list.append(decrypted_bytes)


        return (File_list)

    full_path = pathlib.Path(my_path).joinpath(file_name)
    print(f"\n\tlocation: {full_path}")
    print("\texctracting bytes")
    content = pathlib.Path(full_path).read_bytes()
    print("\treading bytes ok")
    decrypted_bytes = decrypt_any_content(content, key)
    print(f"\t{decrypted_bytes}")
    return (decrypted_bytes)


def create_file(message, encrypted):
    '''cette fonction pourrait être généralisée d'avantage, elle sert à écrire un contenu texte déjà extrait, dans un
    nouveau fichier texte. Si l'utilisateur ne veut pas assigner de nom particulier au fichier, le contenu est copier
     dans un fichier commun'''
    while True:
        filename = input("\n\tPlease choose a name for your file"
                         " or press enter to save it in the common ecnrypted log file:\n Filename (or press enter):")

        if filename == "":
            encrypt_log = open("Common_log.txt", "a")
            encrypt_log.write(f"\n{message}:{encrypted}")
            print(f"\n\tyour message has been successfully appended to the Common_log file see in: {os.getcwd()}")
            break
            return (encrypt_log.read())


        else:
            if check_extension(filename, ".txt"):
                if os.path.isfile(os.path.join(os.getcwd(), filename)):
                    print(
                        f"\n\tThe file {os.path.join(os.getcwd(), filename)} already exists, the text has been appended to it")
                    appendToFile = open(f"{filename}", "a")
                    appendToFile.write(f"{message}:{encrypted}")
                    break
                    return (appendToFile.read())
                else:
                    new_file = open(f"{filename}", "w")
                    new_file.write(f"{message}:{encrypted}")
                    new_file.close()
                    print(f"\n\tyour message has been successfully saved as {filename} see in: {os.getcwd()}")
                    open_new_file(filename)
                    break
                    return (new_file)

            else:
                print("\n\tincorrect name: must be of the form 'Name.txt'")


def function_on_full_tree(directory, Myfunction, suffix, p_name, p_crypt, p_key):
    ''' on voudrait généraliser ici l'application d'une fonction à un dossier et son arborescence mais on est encore dans le cas
    particulier de notre programme où les fonctions utilisées doivent s'appliquer au contenu des fichiers.
    directory est un path qui pointe vers un dossier existant, function ici est très spécial se doit être l'une ou l'autre de encrypt ou decrypt
    suffix est soit ".crypt" soit une chaine vide "", p_name est le préfixe au nom de dossier d'arrivée où seront copier nos fichiers finaux,
    dans le cas de decrypt on pourra prendre la chaine vide "". p_crypt est un booléen qui renvoit true si la fonction est encrypt false autrement  '''
    print("trying new function")

    my_path = pathlib.Path(directory).parent  # on extrait le chemin parent

    dir_name = pathlib.Path(directory).name  # on extrait le nom du dossier en question

    Mytree_list = tree_list(
        directory)  # tree_list renvoie une liste de deux listes, la première avec les chemins d'accés au fichier,
    # la seconde avec le nom des fichiers
    Name_list = Mytree_list[
        1]  # on récupère donc les noms de fichiers deuxième élément de tree_list (une liste est indexée à partir de 0)
    true_pathlist = Mytree_list[
        0]  # ici on récupère donc la liste des vrais chemins de fichiers, premier élément indice 0 de tree_list

    ''' on a besoin d'attribuer un suffixe .crypt a tous les fichiers sans extensions (dans le cas de cryptage de dossier)
    ou le suffixe vide "" pour supprimer l'extension .crypt aux fichiers qui s'en sont vu attribuer une (dans le cas de decryptage)
    on doit le faire ici car la verification de l'existence d'une extension est le seul moyen de tester
    nos chemins de fichier comme des fichiers (potentiels) et
    pointant vers les dossiers encore vide. La fonction is_file() ne peut pas être utilisé
    car le fichier n'existe pas encore. Il faut donc faire l'opération is_file sur les vrais
    chemins. On peut ainsi vérifier que l'on a affaire à un fichier.'''
    if p_crypt:
        temp_list = add_extension(true_pathlist, f"{suffix}")
        true_pathlist = temp_list
        temp_list = []  # on libère la mémoire tant qu'à faire.
        new_name = f"{p_name}{dir_name}"
        print(f"\n\tdirectory name:{dir_name}")
    else:
        split = dir_name.split("crypt_")  # on veut supprimer ici le préfixe du dossier "crypt_" s'il existe.
        if split[0] == "":
            new_name = split[1]
        else:
            new_name = split[0]

        print(f"\n\tdirectory name:{dir_name}")

    print(f"{true_pathlist}")

    print("trying MyFunction parameter")
    en_de_crypted_content = Myfunction(dir_name, my_path,
                                       p_key)  # on encrypte ou decrypt le contenu de chaque fichier avec
    # cette nouvelle fonction qui reconnaît un dossier
    # et sait lire les bytes de chaque fichier
    # pour les encrypter et on récupère une liste de contenus
    # encryptés ou decryptés
    ''' une fois le contenu des fichiers du dossier encrypté ou decrypté on veut recréer l'arborescence du dossier de départ dans le dossier
    d'arrivée, pour cela on utlise nos fonctions mklist_subdir qui renvoie la liste des sous-chemins pointant vers les fichiers sources
    et mklist_new_tree qui renvoi la list des chemins concaténé avec le chemin du dossier d'arrivée.
    Il nous faut d'abord créé le dossier d'arrivé pour nos fichiers encrypté '''

    # quelque soit le nom on a besoin du chemin pointant vers le dossier en question
    path_new_dir = pathlib.Path(pathlib.Path.cwd() / f"{new_name}")  # on crée un chemin pointant
    # vers le nouveau dossier
    # on crée le dossier au chemin voulu en vérifiant qu'un dossier n'est pas déjà existant à ce chemin
    if path_new_dir.exists():
        overwrite_dir = confirmation(f"\n\tDo you want to overwrite the existing directory at {path_new_dir} ?")
        if not overwrite_dir:

            print("\n\ttry another path then")
            return ([])
        else:
            new_dir = path_new_dir.mkdir(
                exist_ok=True)  # la permission est donnée d'écraser les dossiers et sous-dossiers existants
    else:
        new_dir = os.mkdir(path_new_dir)  # dans le cas où le dossier n'existait pas on peut le créer librement

    list_subdir = mklist_subdir(directory,
                                true_pathlist)  # on crée la liste des sous-chemins d'arborescence tirés du dossier source
    list_new_tree = mklist_new_tree(path_new_dir, list_subdir)  # on crée notre nouvelle liste de chemin de fichier

    print(list_new_tree)
    # pointant vers le nouveau dossier source
    # now we need to create all subdirectories before copying our files
    list_new_subdir_path = parent_path(list_new_tree)  # this gives us all subdirs path
    print(list_new_subdir_path)

    for i in list_new_subdir_path:
        if pathlib.Path(i).exists():  # on pourrait ajouter simplement
            # le param mkdir(exist_ok=True) mais on ne veut pas prendre le risque d'écraser un
            # dossier existant.
            print("this directory already exists. passing...")

        else:

            pathlib.Path(i).mkdir(
                parents=True)  # l'option parents=True permet de créer tous les sous-dossiers intermédiaires

        # c'est cette dernière liste qui doit servir de chemin pour créer nos nouveaux fichiers encrypté.

        # bytes_crypt_content = print(f"bytes encrypted as: {encrypted_content}")
    return ([en_de_crypted_content, list_new_tree,
             path_new_dir])  # on peut avoir besoin de ces 3 choses, le contenu des fichiers,
    # liste des chemins d'arborescence pointant vers tous les sous dossiers du nouveau dossier, et le chemin du nouveau dossier.


def type_and_encrypt(key):
    '''cette fonction permet de taper directement le texte dans l'invite de commande
    avant de l'encrypter. On indique la fin du fichier par le signal EOF ctrl-Z (Win) ou ctrl-D (Unix)'''

    with open('tempfile', "w") as fp:
        buffer = ""
        print("\n\n\ttype your text here:")
        while True:
            try:
                line = input("\n\tnewline:")
            except EOFError:
                break
            if not line:
                print("\n\tsend an EOF Signal when your message is complete. (Win:Ctrl-Z ; Unix:Ctrl-D)")

            content = buffer + f"\n{line}"
            fp.write(content)
        fp.close()

        message = open('tempfile', 'r').read()
        os.remove('tempfile')

    message = message.encode("Utf8")
    encrypted = encrypt_message(message, key)
    print(f"\n\there is your encrypted message: {encrypted}")
    while True:
        save = input("\n\tdo you want to save it in a particular .txt file ?\n\t'y' or 'n'(= exit):\n\t#Crypto>")
        if save == 'y':
            create_file(message.decode("Utf8"), encrypted)
            break
        elif save == 'n':
            goodbye()
            time.sleep(1)
            break
            sys.exit(0)
        else:
            print("\n\tselect 'y' or 'n' plz.")


def encrypt_file(key):
    ''' cette fonction est en réalité un programme complet et devrait être
    redécoupée en sous fonctions plus élémentaires elle devrait aussi être
    renommée car elle permet aussi de crypter un dossier complet en
    recréant toute l'arborescence du dossier source '''

    input_path = ""
    real_path = ""
    text_encrypted = False
    bytes_encrypted = False
    Name_list = []
    path_new_dir = ""
    show_archive = False
    encrypted_content = ""
    isfile = False
    isdir = False

    while True:
        ''' cette boucle est pleine d'approximations, c'était notre première grosse boucle, on a refait une série de contrôle 'if' au début mais on pourrait 
        encore tout remanier, l'algorithme est foireux. On voulait faire un test sur le fichier car la fonction write() ne fonctionne pas si on ne lui 
        donne pas le bon type (string ou bytes), mais en invoquant la fonction read avec 'rb' il est probable que l'on aurait résolu tous les pbs.
        en tout cas si l'on veut tester si l'on a affaire à des str ou des bytes on pouvait faire beaucoup mieux '''

        ''' la première condition if est une première amélioration de l'originale elle effectue le test voulu de manière
         plus efficace que ce qu'il y avait à l'origine'''
        file_name = input("\n\tspecify the name of the file to encrypt, and press enter:\n\t#Crypto>:")

        if os.path.isfile(file_name):
            isfile = True
            print(f"\n\tencryption of the file:{file_name}")
            break
        elif os.path.isdir(file_name):
            isdir = True
            print(f"\n\tencryption of the directory:{file_name}")
            break
        else:
            print(f"\n\t{file_name} is neither a file nor a directory."
                  "\n\tplease make sure to select a valid existing file or a valid directory.")

    if check_txtFile(file_name):

        try:
            my_path = os.path.normpath(os.getcwd())
            encrypted_content = extract_str_and_encrypt(file_name, my_path, key)
            str_crypt_content = print(encrypted_content)
            text_encrypted = True
            print(encrypted_content)

            # if not os.path.exists(os.path.join(input_path,file_name)):
            #  print("can't find the file in specified directory")
            # file_name = input("select your text file to encrypt")

        except:

            while True:
                try:
                    input_path = input(
                        "\n\tYour file is not in cwd. Select a path to the directory.\n\t\n\t#Crypto> Path:")

                    real_path = os.path.normpath(input_path)
                    encrypted_content = extract_str_and_encrypt(file_name, real_path, key)
                    str_crypt_file = print(encrypted_content)
                    text_encrypted = True

                except:
                    print("\n\tcan't find the file in the selected path.")

                if text_encrypted:
                    break


    elif file_name == "":
        print(f"\n\tyou must enter the name of a file in the current working directory:{os.getcwd()}.\n"
              "you can also select a path pointing to full directory")
    else:
        if os.path.isfile(file_name):
            print(f"\n\tfichier d'extension:{extension_file(file_name)}")
            print("\n\t encryption is now set in bytes mode")
            my_path = pathlib.Path(file_name).parent
            file_name = pathlib.Path(file_name).name
            encrypted_content = extract_bytes_and_encrypt(file_name, my_path, key)
            print(f"\tbytes decrypted as: {encrypted_content}")
            bytes_encrypted = True


        elif os.path.isdir(file_name):
            input(f"\n\tyou chose to encrypt the entire directory {file_name}, press enter to continue.")

            try:
                ''' ici on invoque une fonction spéciale pour: 
                1) extraire l'arborescence d'un dossier source, 
                2)appliquer ensuite une nouvelle fonction voulue à l'ensemble des fichiers du dossier source 
                3) retourner plusieurs choses: 
                    a) une liste contenant à la fois le contenu encrypté des fichiers (sous forme d'une liste),
                    b) les listes de chemins de la nouvelle arborescence dans laquelle devront être créer les nouveaux fichiers cryptés
                    c) le chemin pointant vers le nouveau dossier créé'''
                list_and_content = function_on_full_tree(file_name, extract_bytes_and_encrypt, ".crypt", p_name="crypt_",
                                                         p_crypt=True, p_key=key)
                #tentative de multithreading

                '''on extrait ensuite à l'aide des indices dans le bon ordres les paramètres dont nous auront besoin plus bas'''
                encrypted_content = list_and_content[0]
                list_new_tree = list_and_content[1]
                path_new_dir = list_and_content[2]
                ''' le paramétre suivant nous permet de sortir de la boucle avec l'information voulue pour la condition 'if' suivante'''
                bytes_encrypted = True


            except:
                print(f"\n\t Could not encrypt the directory:{file_name} .")

    if text_encrypted:
        try:
            while True:

                if os.path.isfile(os.path.join(os.getcwd(), "Crypt_"f"{file_name}")):
                    choix = input(
                        f"\n\tDo you want to overwrite the existing file 'Crypt_{file_name}'?\n\ttype 'y' or 'n' and press enter:\n\t#Crypto>")
                    if choix == "y":
                        break

                    elif choix == "n":

                        while True:
                            file_name = input(
                                "\n\tselect another name for the crypted file and press enter\n Filename:")

                            if check_extension(file_name, ".txt"):
                                break
                            else:
                                print("\n\tplease enter a name in the form name.txt\nagain")
                        break



                    else:
                        print("\n\tplease select 'y' or 'n'")

                else:
                    break

            # to make sure we use the name of the file and not the path c:/users/.../file.txt
            filename = pathlib.Path(file_name).stem
            file_ext = pathlib.Path(file_name).suffix
            newName = f"Crypt_" + f"{filename}" + f"{file_ext}"

            crypt_file = open(newName, "w")
            content = encrypted_content
            crypt_file.write(content.decode(
                "Utf8"))  # attention sans l'option "decode" il est impossible d'écrire le fichier car l'argument n'est pas une string
            crypt_file.close()
            print(f"\n\tYour file has been crypted and save as {newName}")
            print("\n\tsee the result of the encryption above")
            open_new_file(newName)
            goodbye()

        except:
            print("\n\tcould not create a cryptfile corresponding to your original file\n")
            print("\n\tsee the result of the encryption above. You can copy it in a newfile manually")


    elif bytes_encrypted:

        ''' ici il faut bien voir que deux cas vont se présenter. Le cas trivial de cryptage d'un fichier simple et celui plus complexe du cryptage
        d'un dossier complet. Pour ce dernier cas nous avons pris soin auparavant de créer des listes de chemins pointant vers nos fichiers sources,
        on en a extrait le contenu, on l'a encrypté et mis dans une autre liste que nous avons récupéré également,
        à présent on veut créer de nouveaux fichiers avec le contenu encrypté et les placer dans le dossier dont l'arborescence a été reproduite 
        à l'identique du dossier source.   '''

        if isinstance(encrypted_content, list):
            '''voici notre liste des contenus cryptés des fichiers source dans le bon ordre'''

            iterlist = list(encrypted_content)
            i = 0
            ''' ce compteur va nous servir à associer à chaque contenu crypté de la liste le bon chemin pointant vers le fichier dans
            lequel le contenu va être écrit'''

            for content in iterlist:
                # newName = Name_list[i] si on avait voulu changer les noms des fichiers
                # cela aurait été utile mais avec nos nouvelles listes,
                # list_new_tree notamment, c'est inutile,
                # on peut directement assigner le bon chemin d'accés
                # au fichier et l'ouvrir au bon endroit
                # avant de copier le contenu encrypté.

                # crypt_file = open(newName, 'wb')
                newName = pathlib.Path(list_new_tree[i])  # les éléments de cette liste doivent être les chemins voulus
                # Attention à l'ordre des noms de fichier dans la liste et au contenu que l'on recopie dedans, par construction il est identique.
                crypt_file = open(newName, 'wb')
                crypt_file.write(content)
                crypt_file.close()
                # pathlib.Path(newName).replace(path_new_dir/f'{newName}') on n'a plus besoin de déplacer les fichiers
                # on les a créé directement au bon endroit.
                i += 1
               # print(f"\n\t writing encrypted content of file /.../{newName.parent.name}/{newName.name}:\n")
               # print(f"\t{content}")
               # print(f"\n\tYour file has been crypted and save as {newName}.")
               # print("\tsee the result of the encryption above.")
            os.chdir(path_new_dir)
            archive = make_archive(str(path_new_dir),
                                   "zip")  # attention make_archive est importée à partir du module shutil
            print("\n\n\t une archive .zip de votre dossier crypté a été créée en plus du dossier normal par commodité")
            show_archive = True

        else:
            '''création du fichier crypté sauvegardé avec un nouveau nom de fichier '''
            # function(file_name,encrypted_content,prefix)
            filename = pathlib.Path(file_name).stem
            file_ext = pathlib.Path(file_name).suffix
            newName = f"Crypt_" + f"{filename}" + f"{file_ext}"

            crypt_file = open(newName, "wb")
            content = encrypted_content
            crypt_file.write(content)
            crypt_file.close()
            print(f"\n\tYour file has been crypted and save as {newName}")
            print("\n\tsee the result of the encryption above")

        '''ici on fait une archive.zip de notre dossier crypté, elle est sauvegardée dans le 'cwd' on pourrait supprimer le dossier non zipé
        mais cela dépend de ce que l'on veut faire, pour l'instant on garde les deux.'''

        if show_archive:
            print("\n\tplease wait until the archive is ready")
            time.sleep(3)
            subprocess.Popen(args=['c:\\', f'{archive}'], executable='C:\\Windows\\explorer.exe')


    else:
        print("\n\tERROR:")
        if isfile:
            print(f"\n\t\tcould not encrypt the selected file: {file_name}.\n")
        elif isdir:
            print(f"\n\tcould not encrypt the selected directory: {file_name}.\n")

    return (encrypted_content)


def decrypt_directory(directory, key):
    ''' fonction invoquée par la fonction decrypt_file si l'input pointe vers un dossier et non un fichier.
    Le sens de la fonction est assez clair, l'algorithme peut être pas. On utilise une fonction spéciale function_on_full_tree pour alléger le code
    ici. Cette fonction est un peu spéciale, allez voir la doc à son sujet en commentaire. En gros elle crée une nouvelle arborescence qui imite
     celle du dossier source et renvoie les listes dont on a besoin pour à écrire dans les nouveaux fichiers.'''

    if os.path.isdir(directory):
        try:
            ''' ici on invoque une fonction spéciale pour extraire l'arborescence d'un dossier source, appliquer ensuite la fonction voulue
            à l'ensemble des fichiers et retourner une liste contenant à la fois le contenu encrypté des fichiers (sous forme d'une liste),
            les listes de chemins de la nouvelle arborescence dans laquelle devront être créer les nouveaux fichiers cryptés ainsi que le
            chemin pointant vers le nouveau dossier créé'''
            list_and_content = function_on_full_tree(directory, extract_bytes_and_decrypt, suffix="", p_name="",
                                                     p_crypt=False, p_key=key)
            '''on extrait ensuite à l'aide des indices dans le bon ordres les paramètres dont nous auront besoin plus bas'''
            decrypted_content = list_and_content[0]
            list_new_tree = list_and_content[1]
            path_new_dir = list_and_content[2]
            ''' le paramétre suivant nous permet de sortir de la boucle avec l'information voulue pour la condition 'if' suivante'''
            bytes_encrypted = True


        except:
            print(
                f"\n\t Could not decrypt the directory:{directory}.\n\n\tCheck the key file and the other arguments of the main function\n")
            return (False)

        iterlist = list(decrypted_content)
        i = 0
        ''' ce compteur va nous servir à associer à chaque contenu crypté de la liste le bon chemin pointant vers le fichier dans
        lequel le contenu va être écrit'''

        for content in iterlist:
            # newName = Name_list[i]    si on avait voulu changer les noms des fichiers
            # cela aurait été utile mais avec nos nouvelles listes,
            # list_new_tree notamment, c'est inutile,
            # on peut directement assigner le bon chemin d'accés
            # au fichier et l'ouvrir au bon endroit
            # avant de copier le contenu encrypté.
            # crypt_file = open(newName, 'wb')
            newName = pathlib.Path(list_new_tree[i])  # les éléments de cette liste doivent être les chemins voulus
            # Attention à l'ordre des noms de fichier dans la liste et au contenu que l'on recopie dedans, par construction il est identique.
            crypt_file = open(newName, 'wb')
            crypt_file.write(content)
            crypt_file.close()
            # pathlib.Path(newName).replace(path_new_dir/f'{newName}') on n'a plus besoin de déplacer les fichiers
            # on les a créé directement au bon endroit.
            i += 1
            print(f"\n\t writing decrypted content of file /.../{newName.parent.name}/{newName.name}:\n")
            try:
                print(f"\t{content}")
            except:
                pass
            print(f"\n\tYour file has been decrypted and save as {newName}.")
            print("\tsee the result of the decryption above.")

            print("\n\ttrying to erase extension '.crypt'")
            # si on veut decrypter les fichiers il faut supprimer l'extension .crypt des fichiers d'arrivée qui était au départ sans extension.
        temp_list = []
        temp_list_ext = []
        for i in list_new_tree:
            if pathlib.Path(i).suffix == ".crypt":
                # i = pathlib.Path(i).with_suffix("")
                del_suffix = pathlib.Path(i).with_suffix("")
                pathlib.Path(i).rename(del_suffix)

                print("\n\tsuffix '.crypt' deleted, no extension file instead")
            else:
                pass

        os.chdir(path_new_dir)
        archive = make_archive(str(path_new_dir),
                               "zip")  # attention make_archive est importée à partir du module shutil
        print("\n\n\t une archive .zip de votre dossier crypté a été créée en plus du dossier normal par commodité")
        show_archive = True
        return ([decrypted_content, archive, show_archive, path_new_dir])

    else:
        print("please make sure to select a directory and try again")
        return ([])


def decrypt_file(key):
    decrypt = False
    input_path = ""
    real_path = ""
    decrypted_content = ""
    text_decrypted = False
    bytes_decrypted = False
    decrypt_dir = False
    abort = False
    isfile = False
    isdir = False

    while True:

        file_name = input("\n\tspecify the name of the file to decrypt, and press enter:\n\t#Crypto>:")

        if os.path.isfile(file_name):
            isfile = True
            print(f"\n\tdecryption of the file:{file_name}")
            break
        elif os.path.isdir(file_name):
            isdir = True
            print(f"\n\tdecryption of the directory:{file_name}")
            break
        else:
            print(f"\n\t{file_name} is neither a file nor a directory."
                  "\n\tplease make sure to select a valid existing file or a valid directory.")

    if check_txtFile(file_name):

        try:
            my_path = os.path.normpath(os.getcwd())
            decrypted_content = extract_str_and_decrypt(file_name, my_path, key)
            if os.path.isfile(file_name):
                file_name = os.path.basename(file_name)
                print(file_name)
            text_decrypted = True
            print(f"\n\t{decrypted_content}")

            # if not os.path.exists(os.path.join(input_path,file_name)):
            #  print("can't find the file in specified directory")
            # file_name = input("select your text file to encrypt")

        except:

            try:
                input_path = input("\n\tyour file is not in cwd. Select a path to the directory")

                real_path = os.path.normpath(input_path)
                decrypted_content = extract_str_and_decrypt(file_name, real_path, key)
                str_decrypt_file = print(decrypted_content)
                print(type(decrypted_content))
                text_decrypted = True


            except:
                print("\n\tcan't find the file in current directory")

    else:
        if os.path.isfile(file_name):
            print(f"\n\tfichier d'extension:{extension_file(file_name)}")

            try:

                my_path = pathlib.Path(file_name).parent
                file_name = pathlib.Path(file_name).name
                decrypted_content = extract_bytes_and_decrypt(file_name, my_path, key)
                print(f"\tbytes decrypted as: {decrypted_content}")
                bytes_decrypted = True


            except:
                print("\n\t Could not decrypt bytes.")


        elif os.path.isdir(file_name):
            input(f"\n\tyou chose to decrypt the entire directory {file_name}, press enter to continue.")
            decrypt_function = decrypt_directory(file_name, key)

            if decrypt_function:
                decrypt_dir = True
            else:
                print("\n\tthere was an error in the attempt of decrypting your directory."
                      "\n\tPlease make sure to use the key file corresponding to the encryption and try again.")
                abort = True

    if text_decrypted:

        if os.path.isfile(
                file_name):  # ce test qui sert à extraire du chemin d'accès le nom de fichier à utiliser est nécessaire car l'utilisateur avait
            # la possibilité d'entrer un simple nom de fichier ou un chemin complet auquel cas la variable file_name n'est pas
            # directement utilisable comme nom de fichier...
            file_name = os.path.basename(file_name)

        '''on ne veut pas toujours ajouter le préfixe 'Decrypt_*' devant le nom de fichier, on peut vouloir simplement retrouver
        le nom de fichier original si celui-ci a déjà reçu le préfixe 'Crypt_*' '''
        split = file_name.split("Crypt_")
        if split[
            0] == "":  # avec split si le nom de fichier contenait bien le préfixe 'Crypt_' le premier indice de la liste sera la chaine vide "",
            # au contraire s'il ne contenait pas ce préfixe le nom reste inchangé et split renvoie la liste [nom.txt]
            print("prefix 'Crypt_*' removed")
            newName = split[1]
            print(f"the crypted file {file_name} has been renamed with the original name: {newName}")
            time.sleep(1)
        else:
            newName = split[0]

        save_file = os.path.join(os.getcwd(), f'{newName}')
        print(save_file)

        # on a tout de suite un test pour savoir si l'on veut ou non écraser un fichier existant.
        #
        if os.path.isfile(save_file):

            overwrite = confirmation(f"\n\t The file {save_file} already exists, do you want to overwrite it ?\n\t")
            if overwrite:

                pass

            else:
                newName = "Decrypt_" + f"{newName}"
                print(f"\n\tthe name has been automatically changed as:{newName}.")
                time.sleep(1)

        decrypt_file = open(newName, "w")
        content = decrypted_content
        decrypt_file.write(content.decode(
            "Utf8"))  # attention sans l'option "decode" il est impossible d'écrire le fichier car l'argument n'est pas une string
        decrypt_file.close()
        print(f"\n\tYour file has been decrypted and save as {newName}")
        print("\n\tsee the result of the encryption above")

        open_new_file(newName)



    elif bytes_decrypted:

        filename = pathlib.Path(file_name).stem
        file_ext = pathlib.Path(file_name).suffix
        newName = f"Decrypt_" + f"{filename}" + f"{file_ext}"

        decrypt_file = open(newName, "wb")
        content = decrypted_content
        decrypt_file.write(
            content)  # attention sans l'option "decode" il est impossible d'écrire le fichier car l'argument n'est pas une string
        decrypt_file.close()
        print(f"\n\tYour file has been decrypted and save as {newName}")
        print("\n\topening your new file...")
        time.sleep(1)
        open_new_file(newName)


    elif decrypt_dir:
        ''' pour ouvrir l'archive créée par la fonction decrypt_directory on a mis dans la variable decrypt_function la liste 
        que renvoie précisément notre fonction decrypt directory, celle-ci contient les arguments voulus archive et show_archive'''
        archive = decrypt_function[1]
        show_archive = decrypt_function[2]

        if show_archive:
            print("\n\tplease wait until the archive is ready")
            time.sleep(3)
            subprocess.Popen(args=['c:\\', f'{archive}'], executable='C:\\Windows\\explorer.exe')





    else:
        print("\n\tERROR:")
        if isfile:
            print(
                f"\n\t\tcould not decrypt the selected file: {file_name}. Check the key you used to decryption and try again.\n")
        elif isdir:
            print(
                f"\n\tcould not decrypt the selected directory: {file_name}. Check the key you used to decryption and try again.\n")


def open_notepad(file):
    notepad = "notepad.exe"
    args = ['C:\\', f'{file}']  # BEWARE: with subprocess.Popen the command (args=)
    # must be a sequence like a tuple or a list and note that it is not necessary
    # to insert a full explicit path (the file is not at C:\ at all here !!)
    # whereas the executable is best selected with full explicit path
    execution = subprocess.Popen(args, executable=f"C:\\windows\\notepad.exe")
    return (execution)


def open_new_file(file):
    input("\n\tpress enter to quit and see your new file")
    return (open_notepad(file))


def presentation():
    try:
        Presentation = print(f"\n{open('Readme.txt', 'r').read()}")
        return (Presentation)
    except:
        print("Exception: could not find the presentation File")
        time.sleep(1)
        print("\n\n\tCrypto v.1.0: This is a simple program to encrypt and decrypt a text file."
              "\n\tby Fr. Raphael Boralevi")


if __name__ == "__main__":
    ''' par défaut lancer crypt message revient à lancer la fonction crypt file avec la clé secret.key du dossier
    courant si elle existe'''
    key = load_key('secret.key')
    decrypt_file(key)

