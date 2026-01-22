# GNS - Network Automation Project

Léa Danober, Robin Jenny, Rémi Durand, Élie Gautier

## Description 

**Ressources** : 

- architecture déjà prête (routeurs, interfaces, liens)
- arborescence GNS (`./project_name/project-files/dynamips/router_ids/configs/iX_startup_config.cfg`)
- fichier d'intention décrivant le réseau : AS, routeurs, interfaces des routers et liens entre eux. Pas d'adresses prédéfinies

**Objectifs du script** : 

- lire le fichier d'intention et affecter des adresses (IPv6) aux interfaces des routeurs (GigabitEthernet et Loopback pour BGP)
- écrire les fichiers de configuration des routeurs (fichier `.cfg`) pour que le réseau fonctionne dès l'ouverture du fichier `.gns3` simulant le réseau
- drag and drop bot : placer les fichiers de configuration correctement dans l'arborescence du projet GNS.

**langage** : `python`

## Structure du Projet

### Arborescence

```pgsql
projet/
├── code/
│   └── intent_file.json
│   └── main.py
│   └── other script
└── network/
    ├── network.gns3
    └── project-files/
		├── images/
		└── dynamips/ routers config folders
```

### Intent file 

L'intent file est un fichier json contenant en prremier les relations inter-AS dans `Intent`, et la liste des routeurs par AS, ainsi que leurs interfaces et les voisins qui y sont conectés dans `Structure`. Il a pour but d'être minimaliste. NB : On rajoute un parametre "PROTOCOL" uniquement pour les routers utilisant EBGP (en bordure d'AS).

**Exemple** 
```
{
    "Intent":{
        "AS1":{
            "AS_NAME":"1111",
            "PEERS":["AS2"],
            "PROVIDERS":["AS3"],
            "CLIENTS":["AS4", "AS5"]
        },
        ...
```

```
    "Structure":{
        "AS1":{
            "AS_NAME" : "1111",
            "PROTOCOL": "RIP",
            "ROUTERS":{
                "R11":{
                    "INTERFACES":{
                        "G1/0": {
                            "NEIGHBORS": {"R13": "G1/0"}
                        },
                        "G2/0": {
                            "NEIGHBORS": {"R12": "G2/0"}
                        },
                        "G3/0": {
                            "NEIGHBORS":{"R41":"G3/0"},
                            "PROTOCOL":"EBGP"
                        }
                    }
                },
				...
```


## Utilisation

Une fois le dossier organisé comme décrit plus haut, et l'intentfile écrit 
