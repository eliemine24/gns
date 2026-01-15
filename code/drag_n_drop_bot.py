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




# Récupérer les noms imbuvables des dossier de config
def find_repository_names():
    
    # lire le fichier "project_name"+".gns3"
    # en faire un dictionnaire (json_ton_dict() ça doit fonctionner)
    # récupérer les noms de fichier correspondans aux noms des routeurs ("R1", "R2", etc)
    # renvoyer un un dict ou une liste de tuples {"router_name" : "repository_name"; etc} / [("router_name", "repository_name"), etc]

    pass

# Déplacer un fichier fichier file depuis l'emplacement du script jusqu'à l'emplacement final
def place_file(file, project_path, gns_path, dest_router_folder):
    
    #On crée des chemins proprement pour ne pas avoir de propblèmes si on passe de Linux à Windows
    source = os.path.join(project_path, "code", file)
    destination = os.path.join(gns_path, "dynamips", dest_router_folder)

    shutil.copy(source, destination)

    pass




# TEST omg ça marche (créer un "testfile.py dans le dossier local")
#shutil.move(PATH+"/testfile.py", HPATH+"/")
