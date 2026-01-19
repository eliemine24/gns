import ipaddress
import json
import os



def charger_json_en_dict(chemin_fichier):
    """
    Lit un fichier JSON et le convertit en dictionnaire Python.
    """
    try:
        if not os.path.exists(chemin_fichier):
            print(f"Erreur : Le fichier '{chemin_fichier}' n'existe pas.")
            return None
            
        with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
            donnees = json.load(fichier)
        return donnees
    
    except json.JSONDecodeError:
        print(f"Erreur : Le fichier '{chemin_fichier}' n'est pas un JSON valide.")
        return None

def sauvegarder_dict_en_json(dictionnaire, chemin_destination):
    """
    Prend un dictionnaire et le sauvegarde dans un nouveau fichier JSON.
    """
    try:
        with open(chemin_destination, 'w', encoding='utf-8') as fichier:
            # indent=4 permet d'avoir un fichier lisible (pas tout sur une ligne)
            # ensure_ascii=False permet de garder les accents (ex: é, à)
            json.dump(dictionnaire, fichier, indent=4, ensure_ascii=False)
        print(f"Succès : Le fichier a été sauvegardé sous '{chemin_destination}'")
        
    except Exception as e:
        print(f"Une erreur est survenue lors de la sauvegarde : {e}")






# --- CONFIGURATION DES RÉSEAUX ---
PREFIXES_AS = {
    "AS1": ipaddress.IPv6Network("1111::/48"),
    "AS2": ipaddress.IPv6Network("2222::/48"),
    "INTER_AS": ipaddress.IPv6Network("3333::/48") # Changé en /48 pour pouvoir créer des sous-réseaux /64
}

def extraire_num(nom):
    chiffres = ''.join(filter(str.isdigit, nom))
    return int(chiffres) if chiffres else 0

def generer_registre_complet(donnees):
    registre = {}
    liens_faits = set()
    
    # Compteurs pour découper les sous-réseaux
    index_interne = {"AS1": 1, "AS2": 1}
    index_ebgp = 1 # Compteur global pour les liens entre AS

    # On pré-découpe les sous-réseaux eBGP
    sous_reseaux_ebgp = list(PREFIXES_AS["INTER_AS"].subnets(new_prefix=64))

    for id_as, contenu_as in donnees["Structure"].items():
        prefixe_as = PREFIXES_AS[id_as]
        sous_reseaux_as = list(prefixe_as.subnets(new_prefix=64))

        for nom_r, contenu_r in contenu_as["ROUTERS"].items():
            registre.setdefault(nom_r, {})
            
            # 1. LOOPBACK (Index 0 du préfixe AS)
            registre[nom_r]["LOOPBACK0"] = f"{sous_reseaux_as[0][extraire_num(nom_r)]}/128"

            # 2. INTERFACES PHYSIQUES
            for nom_int, info_int in contenu_r["INTERFACES"].items():
                voisin = list(info_int["NEIGHBORS"].keys())[0]
                int_voisin = info_int["NEIGHBORS"][voisin]
                paire = tuple(sorted((nom_r, voisin)))

                if paire not in liens_faits:
                    # CAS EBGP : Nouveau sous-réseau /64 dédié
                    if info_int.get("PROTOCOL") == "EBGP":
                        net = sous_reseaux_ebgp[index_ebgp]
                        ips = (f"{net[1]}/64", f"{net[2]}/64")
                        index_ebgp += 1
                    # CAS INTERNE : Sous-réseau /64 de l'AS
                    else:
                        net = sous_reseaux_as[index_interne[id_as]]
                        ips = (f"{net[1]}/64", f"{net[2]}/64")
                        index_interne[id_as] += 1
                    
                    registre[paire[0]][nom_int] = ips[0]
                    registre.setdefault(paire[1], {})[int_voisin] = ips[1]
                    liens_faits.add(paire)
                    
    return registre

def generer_plan_adressage(intention):
    registre = generer_registre_complet(intention)
    resultat = {"Intent": {}, "Structure": {}}

    for id_as, contenu_as in intention["Structure"].items():
        resultat["Structure"][id_as] = {
            "AS_NAME": contenu_as["AS_NAME"],
            "PROTOCOL": contenu_as["PROTOCOL"],
            "ROUTERS": {}
        }

        for nom_r, contenu_r in contenu_as["ROUTERS"].items():
            num = extraire_num(nom_r)
            r_data = {"ROUTER_ID": f"{num}.{num}.{num}.{num}", "INTERFACES": {}}

            # Interfaces physiques et eBGP
            for nom_int, info_int in contenu_r["INTERFACES"].items():
                nom_v = list(info_int["NEIGHBORS"].keys())[0]
                int_v = info_int["NEIGHBORS"][nom_v]
                
                r_data["INTERFACES"][nom_int] = {
                    "ADDRESS": registre[nom_r][nom_int],
                    "NEIGHBORS_ADDRESS": [registre[nom_v][int_v]]
                }
                if "PROTOCOL" in info_int: r_data["INTERFACES"][nom_int]["PROTOCOL"] = "EBGP"

            # Ajout Loopback avec tous les autres du même AS (Voisins iBGP)
            autres_lb = [registre[r]["LOOPBACK0"] for r in contenu_as["ROUTERS"] if r != nom_r]
            r_data["INTERFACES"]["LOOPBACK0"] = {
                "ADDRESS": registre[nom_r]["LOOPBACK0"],
                "NEIGHBORS_ADDRESS": autres_lb
            }
            
            resultat["Structure"][id_as]["ROUTERS"][nom_r] = r_data

    return resultat

#Lancement de tests

# Récupère le dossier où se trouve le script .py actuel
dossier_actuel = os.path.dirname(__file__)
chemin_complet = os.path.join(dossier_actuel, "intent_file_2.json")
intention_json = charger_json_en_dict(chemin_complet)
mon_plan = generer_plan_adressage(intention_json)


print(json.dumps(mon_plan, indent=4))

sauvegarder_dict_en_json(mon_plan, "test.json")


