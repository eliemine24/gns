# ============
# === MAIN ===
# ============

from router import Router
from interface import Interface
from generate_classes import *
from write_config import *
from drag_n_drop_bot import find_repository_names

LPATH = find_local_path() + "/"                        # local path
HPATH = os.path.dirname(LPATH.rstrip('/')) + "/"      # local path un cran plus haut (équivalent cd ..)
INTENT = json_to_dict("intent_file.json")             # dictionnaire issu du fichier d'intention
PROJECT_NAME = "projet_test"                           # nom du folder du projet gns3

# juste pour la visualisation
print("--- pathes ---")
print(f"local path : {LPATH}")
print(f"home path : {HPATH}")
print("---------------------")

# génération des classes routeurs et interfaces dans router_list
router_list = generate_network_classes(LPATH + "intent_file.json")

# affichage 
"""
print("--- ROUTERS ---")
for r in router_list:
    print(f"{r.name} (AS {r.AS_name}) | {r.ID} | {r.nb_int}")
    for i in r.liste_int:
        print(f"  {i.name} {i.address} {i.protocol} neighbors: {i.neighbors_address}")
print("---------------")
"""

# écriture cfg 
for r in router_list:
    outfile = LPATH+r.name+ ".cfg"
    write_config(r, outfile, router_list)

# drag n drop tests
REPOS_DICT = find_repository_names(router_list, PROJECT_NAME, HPATH)
print(REPOS_DICT)