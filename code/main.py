# ============
# === MAIN ===
# ============

from router import Router
from interface import Interface
from generate_classes import *
from write_config import *
from drag_n_drop_bot import find_repository_names

LPATH = find_local_path() + "/"                        # /home/elie/insa/3TC/gns/gns/code/
HPATH = os.path.dirname(LPATH.rstrip('/')) + "/"      # /home/elie/insa/3TC/gns/gns/
MAIN_DEST = HPATH + "project-files/dynamips"          # destination générale des .cfg
INTENT = json_to_dict("intent_file.json")       
PROJECT_NAME = "projet_test"

print("--- pathes ---")
print(f"local path : {LPATH}")
print(f"home path : {HPATH}")
print("---------------------")
# génération des routeurs et interfaces
router_list = generate_network_classes(LPATH + "intent_file.json")

# affichage 
"""
for r in router_list:
    print(f"{r.name} (AS {r.AS_name}) | {r.ID} | {r.nb_int}")
    for i in r.liste_int:
        print(f"  {i.name} {i.address} {i.protocol} neighbors: {i.neighbors_address}")
"""

# écriture cfg 
for r in router_list:
    outfile = LPATH+r.name+ ".cfg"
    write_config(r, outfile, router_list)

# drag n drop tests
REPO = find_repository_names(router_list, PROJECT_NAME, HPATH)
print(REPO)