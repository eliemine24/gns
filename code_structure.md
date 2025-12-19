# Structure du code

**ressources** : 
- architecture déjà prête (routeurs, interfaces, liens)
- arborescence GNS (`./project_name/project-files/dynamips/router_ids/configs/iX_startup_config.cfg`)
- fichier network intent (json)

**sortie du programme** : fichier `.cfg` de chaque routeurs du réseau, placé correctement dans l'arborescence (drag & drop bot)

**langage** : `python`

## Découpage

On dispose de classes `routers` et `interfaces` pour stockers touts les infos sur les routers et interfaces

### CONFIGURATION DU RÉSEAU
- Ouverture / lecture du fichier d'intention
- recherche des routeurs dans l'arborescence du GNS
- récupération des noms des routeurs (+ vérification du nb) et (création d'une liste de classes ?)
- (vérification des liens)
- configuration des routeurs = rédaction des .cfg de chaque routeur et placement dans l'arborescence

### CONFIGURATION D'UN ROUTEUR = RÉDACTION DES `.cfg`:
- récupération des infos générales du routeur : noms, nb d'interfaces, protocole(s)
- récupération des infos de chaque interfaces :  @ip, protocol, voisins
- pour chaque routeur : vérifier les protocoles (BGP/OSPF/RIP)
- à chaque fois, stockage dans les classes de noms correspondants
- rédaction du `.cfg` à partir des infos récupérées 
- placement du `.cfg` dans l'arborescence (attention les noms dans l'arborescence sont anonymes)

### RÉDATION DU `.cfg` :
- header
- liste des interfaces
- liste des routers par protocole
- address-family (?)



## À CODER

### Classes

- `router` : name, interfaces_number, interfaces_list, protocols_list
- `interface` : name, address, neighbors_address, protocol

### Fonctions

- `find_local_path()` : trouve l'emplacement du programme et l'exporte
- `json_to_dict(in_file)` : génère un dictionnaire à partir du fhcier d'intention

- `generate_network_classes(int_file)` : lit le fichier d'intention et crée toutes les classes nécessaires pour écrire les configurations
    - `generate_router(int_dict)` : génère un router à partir des infos qu'on lui donne
        - `generate_interfaces(int_dict, router)` génère les classes `interface` du router

- `write_config(router, path_to_router, out_file)` : fonction générale qui écrit une configuration pour un router dans un fichier cfg, contient d'autres fonctions
    - `write_header(router)` : écrit l'en-tête de config
    - `write_interfaces_config(router)` : gère la configuration de tous les interfaces du router (en fonction des protocoles)
        - `write_loopback(interface)` : écrit la partie loopback
        - `write_FE(interface)` : écrit la configuration de fast ethernet
        - `write_GE(interface)` : pareil pour GE
    - `write_bgp_config` : 
        - find a way to write this fckn bgp table 
    - `write_ipv4_address_family` écrit la config @family_ipv4 (non utilisé mais probablement à écrire quand même)
    - `write_ipv6_address_family` : écrit la config ipv6 family (voir fichier de config)
        - problème pour plus tard
- `drag_and_drop_bot(cfg_file, out_path)` : place le fichier généré dans la config gns