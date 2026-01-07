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

PATH = find_local_path()
INTENT = json_to_dict("intent_file.json")
