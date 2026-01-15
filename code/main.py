# ============
# === MAIN ===
# ============

from router import Router
from interface import Interface
from generate_classes import *
from write_config import *

LPATH = find_local_path()                        # chemin du script
HPATH = LPATH.rsplit('/', 1)[0]                  # chemin du projet
MAIN_DEST = HPATH + "/project-files/dynamips"   # destination générale des .cfg
INTENT = json_to_dict("intent_file.json")       # fichier d'intention
PROJECT_NAME = str(input("Nom du dossier contenant le projet : "))

print(f"local path : {LPATH}")

# génération des routeurs et interfaces
router_list = generate_network_classes(local_path + "intent_file.json")

# affichage 
"""
for r in router_list:
    print(f"{r.name} (AS {r.AS_name}) | {r.ID} | {r.nb_int}")
    for i in r.liste_int:
        print(f"  {i.name} {i.address} {i.protocol} neighbors: {i.neighbors_address}")
"""

# test écriture cfg 
for r in router_list:
    outfile = LPATH+r.name+ ".cfg"
    write_config(r, outfile, router_list)
