import ipaddress
import json
import os

# --- VARIABLES GLOBALES ---
AS_CONFIG = {}
EBGP_CONFIG = {}

# --- FONCTIONS UTILES ---

def charger_json_en_dict(chemin_fichier):
    try:
        if not os.path.exists(chemin_fichier):
            print(f"[-] Erreur : Fichier introuvable : {chemin_fichier}")
            return None
        with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
            return json.load(fichier)
    except Exception as e:
        print(f"[-] Erreur lecture JSON : {e}")
        return None

def sauvegarder_dict_en_json(dictionnaire, chemin_destination):
    try:
        with open(chemin_destination, 'w', encoding='utf-8') as fichier:
            json.dump(dictionnaire, fichier, indent=4, ensure_ascii=False)
        print(f"[+] Succès : Sauvegarde dans {chemin_destination}")
    except Exception as e:
        print(f"[-] Erreur sauvegarde : {e}")

def extraire_num(nom):
    chiffres = ''.join(filter(str.isdigit, nom))
    return int(chiffres) if chiffres else 0

# --- LOGIQUE DE GÉNÉRATION ---

def initialiser_topologie(donnees_intent):
    """Analyse l'intention et remplit les variables globales."""
    global AS_CONFIG, EBGP_CONFIG
    
    # On vérifie si la clé 'Structure' existe
    structure = donnees_intent.get("Structure", {})
    if not structure:
        print("[-] ERREUR : La clé 'Structure' est absente du fichier JSON !")
        return

    as_list = list(structure.keys())
    base_ip = 0x1111 
    
    for i, id_as in enumerate(as_list):
        prefixe_str = f"{hex(base_ip + i)[2:]}::/48"
        reseau_principal = ipaddress.IPv6Network(prefixe_str)
        
        AS_CONFIG[id_as] = {
            "NOM_AS": structure[id_as].get("AS_NAME"),
            "PROTOCOLE": structure[id_as].get("PROTOCOL"),
            "RESEAU": reseau_principal,
            "SOUS_RESEAUX": list(reseau_principal.subnets(new_prefix=64)),
            "ROUTEURS": list(structure[id_as].get("ROUTERS", {}).keys())
        }
    
    prefixe_ebgp_str = "9999::/48" 
    reseau_ebgp = ipaddress.IPv6Network(prefixe_ebgp_str)
    EBGP_CONFIG["INTER_AS"] = {
        "RESEAU": reseau_ebgp,
        "SOUS_RESEAUX": list(reseau_ebgp.subnets(new_prefix=64))
    }
    print(f"[+] Topologie initialisée avec {len(AS_CONFIG)} AS.")

def creer_registre_dynamique(donnees_intent):
    registre = {}
    liens_vus = set()
    index_lien_interne = {id_as: 1 for id_as in AS_CONFIG}
    index_ebgp = 0

    for id_as, as_info in AS_CONFIG.items():
        for nom_r in as_info["ROUTEURS"]:
            registre.setdefault(nom_r, {})
            num_r = extraire_num(nom_r)
            lb_net = as_info["SOUS_RESEAUX"][0]
            registre[nom_r]["LOOPBACK0"] = f"{lb_net[num_r + 110]}/128"

            interfaces = donnees_intent["Structure"][id_as]["ROUTERS"][nom_r]["INTERFACES"]
            for nom_int, info_int in interfaces.items():
                voisin = list(info_int["NEIGHBORS"].keys())[0]
                int_voisin = info_int["NEIGHBORS"][voisin]
                paire = tuple(sorted((nom_r, voisin)))

                if paire not in liens_vus:
                    if info_int.get("PROTOCOL") == "EBGP":
                        net = EBGP_CONFIG["INTER_AS"]["SOUS_RESEAUX"][index_ebgp]
                        index_ebgp += 1
                    else:
                        idx = index_lien_interne[id_as]
                        net = as_info["SOUS_RESEAUX"][idx]
                        index_lien_interne[id_as] += 1
                    
                    registre[paire[0]][nom_int] = f"{net[1]}/64"
                    registre.setdefault(paire[1], {})[int_voisin] = f"{net[2]}/64"
                    liens_vus.add(paire)
    return registre

def generer_plan_adressage(intention):
    if not AS_CONFIG:
        print("[-] Erreur : AS_CONFIG est vide. L'initialisation a échoué.")
        return {"Intent": {}, "Structure": {}}

    registre = creer_registre_dynamique(intention)
    resultat = {"Intent": {}, "Structure": {}}

    for id_as, info_as in AS_CONFIG.items():
        resultat["Structure"][id_as] = {
            "AS_NAME": info_as["NOM_AS"],
            "PROTOCOL": info_as["PROTOCOLE"],
            "ROUTERS": {}
        }
        routeurs_source = intention["Structure"][id_as]["ROUTERS"]

        for nom_r, contenu_r in routeurs_source.items():
            num = extraire_num(nom_r)
            r_data = {"ROUTER_ID": f"{num}.{num}.{num}.{num}", "INTERFACES": {}}

            for nom_int, info_int in contenu_r["INTERFACES"].items():
                nom_v = list(info_int["NEIGHBORS"].keys())[0]
                int_v = info_int["NEIGHBORS"][nom_v]
                r_data["INTERFACES"][nom_int] = {
                    "ADDRESS": registre[nom_r][nom_int],
                    "NEIGHBORS_ADDRESS": [registre[nom_v][int_v]]
                }
                if "PROTOCOL" in info_int: r_data["INTERFACES"][nom_int]["PROTOCOL"] = "EBGP"

            autres_lb = [registre[a]["LOOPBACK0"] for a in info_as["ROUTEURS"] if a != nom_r]
            r_data["INTERFACES"]["LOOPBACK0"] = {
                "ADDRESS": registre[nom_r]["LOOPBACK0"],
                "NEIGHBORS_ADDRESS": autres_lb
            }
            resultat["Structure"][id_as]["ROUTERS"][nom_r] = r_data
    return resultat

# --- EXECUTION ---

# --- DIAGNOSTIC ---
dossier = os.path.dirname(os.path.abspath(__file__))
f_entree = os.path.join(dossier, "intent_file_2.json")

intent = charger_json_en_dict(f_entree)

if intent:
    print(f"Clés trouvées à la racine du JSON : {list(intent.keys())}")
    
    # On force la détection de la clé de structure
    cle_structure = "Structure" if "Structure" in intent else "structure"
    
    if cle_structure in intent:
        print(f"Succès : Clé '{cle_structure}' trouvée !")
        # On peut relancer l'initialisation
        initialiser_topologie(intent)
        mon_plan = generer_plan_adressage(intent)
        sauvegarder_dict_en_json(mon_plan, "test.json")
    else:
        print("ERREUR CRITIQUE : Aucune clé 'Structure' ou 'structure' trouvée.")
        print("Voici le contenu du fichier pour t'aider :", intent)