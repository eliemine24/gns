# ============
# === MAIN ===
# ============

from router import Router
from interface import Interface
from generate_classes import *
from write_config import *


# trouver le chemin local
local_path = find_local_path()
local_path = local_path+"/"
print(f"local path : {local_path}")

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
    outfile = local_path+r.name+ ".cfg"
    write_config(r, outfile)
