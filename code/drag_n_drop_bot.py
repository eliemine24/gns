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
    # Path: /home/elie/insa/3TC/gns/gns/ + projet_test/ + projet_test.gns3
    gns3_file = os.path.join(general_path, project_name, f"{project_name}.gns3")
    project_dict = json_to_dict(gns3_file)
    
    nodes = project_dict.get("topology", {}).get("nodes", [])
    
    for router in routers_list:
        for node in nodes:
            if node.get("name") == router.name:
                repo_name = node.get("node_id")
                if repo_name:
                    repo_names[router.name] = repo_name
                break
    
    return repo_names

# Déplacer un fichier fichier file depuis l'emplacement du script jusqu'à l'emplacement final
def place_file(file, project_path, gns_path, dest_router_folder):
    
    #On crée des chemins proprement pour ne pas avoir de propblèmes si on passe de Linux à Windows
    source = os.path.join(project_path, "code", file)
    destination = os.path.join(gns_path, "dynamips", dest_router_folder)

    shutil.copy(source, destination)