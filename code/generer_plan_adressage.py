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




# --- CONFIGURATION DES RÉSEAUX DE BASE ---
PREFIXES_AS = {
    "AS1": ipaddress.IPv6Network("1111::/48"),
    "AS2": ipaddress.IPv6Network("2222::/48"),
    "INTER_AS": ipaddress.IPv6Network("3333::/64")
}

def extraire_numero_routeur(nom):
    """Récupère le numéro dans le nom du routeur (ex: 'R12' -> 12)."""
    chiffres = ''.join(filter(str.isdigit, nom))
    return int(chiffres) if chiffres else 0

def generer_ip_loopback(nom_as, nom_routeur):
    """Génère une Loopback unique (Format: AS:3::11X)."""
    num = extraire_numero_routeur(nom_routeur)
    # On prend le premier sous-réseau /64 de l'AS, et on modifie le 4ème quartet pour le '3'
    base = str(PREFIXES_AS[nom_as][0]).replace('::', f':3::11{num}')
    return f"{base}/128"

def creer_registre_adresses(donnees_intention):
    """
    Parcourt le fichier d'intention pour calculer et stocker 
    toutes les adresses dans un registre central.
    """
    registre = {}
    liens_termines = set()
    index_liens = {"AS1": 1, "AS2": 1}

    # On explore chaque AS dynamiquement
    for id_as, contenu_as in donnees_intention["Structure"].items():
        for nom_r, contenu_r in contenu_as["ROUTERS"].items():
            registre.setdefault(nom_r, {})
            
            # 1. Attribution de la Loopback
            registre[nom_r]["LOOPBACK0"] = generer_ip_loopback(id_as, nom_r)

            # 2. Attribution des interfaces physiques
            for nom_int, info_int in contenu_r["INTERFACES"].items():
                # On identifie le voisin
                voisin = list(info_int["NEIGHBORS"].keys())[0]
                interface_voisin = info_int["NEIGHBORS"][voisin]
                
                # Identifiant unique du lien (indépendant de l'ordre)
                paire_lien = tuple(sorted((nom_r, voisin)))

                if paire_lien not in liens_termines:
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
                    
                    # On enregistre l'IP pour le routeur A et le routeur B
                    registre[paire_lien[0]][nom_int] = ips[0]
                    registre.setdefault(paire_lien[1], {})[interface_voisin] = ips[1]
                    
                    liens_termines.add(paire_lien)
    return registre

def formater_routeur(nom_r, contenu_r, registre, liste_routeurs_as):
    """Construit le dictionnaire final pour un routeur donné."""
    num = extraire_numero_routeur(nom_r)
    
    donnees_finales = {
        "ROUTER_ID": f"{num}.{num}.{num}.{num}",
        "INTERFACES": {}
    }

    # Interfaces physiques
    for nom_int, info_int in contenu_r["INTERFACES"].items():
        nom_voisin = list(info_int["NEIGHBORS"].keys())[0]
        int_voisin = info_int["NEIGHBORS"][nom_voisin]
        
        details = {
            "ADDRESS": registre[nom_r][nom_int],
            "NEIGHBORS_ADDRESS": [registre[nom_voisin][int_voisin]]
        }
        # On conserve les propriétés optionnelles
        if "PROTOCOL" in info_int: details["PROTOCOL"] = info_int["PROTOCOL"]
        if "COST" in info_int: details["COST"] = info_int["COST"]
        
        donnees_finales["INTERFACES"][nom_int] = details

    # Loopback (Voisins iBGP = tous les autres routeurs de la même AS)
    voisins_ibgp = [registre[autre]["LOOPBACK0"] for autre in liste_routeurs_as if autre != nom_r]
    donnees_finales["INTERFACES"]["LOOPBACK0"] = {
        "ADDRESS": registre[nom_r]["LOOPBACK0"],
        "NEIGHBORS_ADDRESS": voisins_ibgp
    }

    return donnees_finales

def generer_plan_adressage(intention):
    """Fonction principale qui transforme l'intention en plan d'adressage."""
    registre = creer_registre_adresses(intention)
    resultat = {"Intent": {}, "Structure": {}}

    for id_as, contenu_as in intention["Structure"].items():
        resultat["Structure"][id_as] = {
            "AS_NAME": contenu_as["AS_NAME"],
            "PROTOCOL": contenu_as["PROTOCOL"],
            "ROUTERS": {}
        }
        
        dictionnaire_routeurs = contenu_as["ROUTERS"]
        for nom_r, contenu_r in dictionnaire_routeurs.items():
            # Génération dynamique basée sur la liste des routeurs de cette AS
            resultat["Structure"][id_as]["ROUTERS"][nom_r] = formater_routeur(
                nom_r, contenu_r, registre, list(dictionnaire_routeurs.keys())
            )

    return resultat


#Lancement de tests

# Récupère le dossier où se trouve le script .py actuel
dossier_actuel = os.path.dirname(__file__)
chemin_complet = os.path.join(dossier_actuel, "intent_file_2.json")
intention_json = charger_json_en_dict(chemin_complet)
mon_plan = generer_plan_adressage(intention_json)


print(json.dumps(mon_plan, indent=4))

sauvegarder_dict_en_json(mon_plan, "test.json")


