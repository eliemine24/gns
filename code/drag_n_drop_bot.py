# =======================
# === DRAG & DROP BOT ===
# =======================

# place les fichier de config dans l'arborescence du projet gsn
# on considère que le script se situe dans un dossier parallèle 
# ./
#   code/
#        scripts, intent_file, etc
#   projet_gns/
#              config_files, etc

from generate_classes import find_local_path, json_to_dict
from datetime import datetime
import os
import shutil #librairie pour la gestion de fichiers

PATH = find_local_path()                        # chemin du script
HPATH = PATH.rsplit('/', 1)[0]                  # chemin du projet
MAIN_DEST = HPATH + "/project-files/dynamips"   # destination générale des .cfg
INTENT = json_to_dict("intent_file.json")       # fichier d'intention
#PROJECT_NAME = str(input("Nom dossier contenant le projet : "))


# Récupérer les noms imbuvables des dossier de config

def find_repository_names(path):
    pass

# Déplacer les fichier au bon endroit jsp comment
def place_files(path):
    pass


# TEST omg ça marche (créer un "testfile.py dans le dossier local")
shutil.move(PATH+"/testfile.py", HPATH+"/")
