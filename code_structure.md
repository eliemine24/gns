# Structure du code

**ressources** : architecture déjà prête (routeurs, interfaces, liens), arborescence GNS ("./project_name/project-files/dynamips/router_ids/configs/iX_startup_config.cfg"), fichier network intent (json)

**sortie du programme** : fichier .cfg de chaque routeurs du réseau, placé correctement dans l'arborescence (drag & drop bot)

**langage** : python

## Découpage

création des classes "routers" et "interfaces" pour stockers touts les infos sur les routers et interfaces

### CONFIGURATION DU RÉSEAU
- Ouverture / lecture du fichier d'intention
- recherche des routeurs dans l'arborescence du GNS
- récupération des noms des routeurs (+ vérification du nb) et (création d'une liste de classes ?)
(- vérification des liens)
- configuration des routeurs = rédaction des .cfg de chaque routeur et placement dans l'arborescence

### CONFIGURATION D'UN ROUTEUR = RÉDACTION DES .cfg:
- récupération des infos générales du routeur : noms, nb d'interfaces, protocole(s)
- récupération des infos de chaque interfaces :  @ip, protocol, voisins
- pour chaque routeur : vérifier les protocoles (BGP/OSPF/RIP)
- à chaque fois, stockage dans les classes de noms correspondants
- rédaction du .cfg à partir des infos récupérées 
- placement du .cfg dans l'arborescence (attention les noms dans l'arborescence sont anonymes

### RÉDATION DU .cfg :
- header
- liste des interfaces
- liste des routers par protocole
- address-family (?)
