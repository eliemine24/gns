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
def find_repository_names(routers_list, project_name, general_path):
    repo_names = {}
    project_dict = json_to_dict(general_path + project_name + ".gns3")
    
    # GNS3 file structure: topology > nodes 
    nodes = project_dict.get("topology", {}).get("nodes", [])
    
    for router in routers_list:
        for node in nodes:
            if node.get("name") == router.name:
                # Extract repository name from the node
                # GNS3 typically stores the compute_id or other identifier
                repo_name = node.get("node_id") or node.get("compute_id")
                if repo_name:
                    repo_names[router.name] = repo_name
                break
    
    return repo_names

# Déplacer un fichier fichier file depuis l'emplacement du script jusqu'à l'emplacement final
def place_file(file, project_path, path_to_file):
    pass




# TEST omg ça marche (créer un "testfile.py dans le dossier local")
#shutil.move(PATH+"/testfile.py", HPATH+"/")
