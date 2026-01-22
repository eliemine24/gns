# GNS - Network Configuration Generator

Un projet Python permettant de générer automatiquement les fichiers de configuration pour des routeurs dans GNS3 à partir d'un fichier d'intention en `.json`.

## Description du Projet

Ce projet automatise la création et la configuration d'un réseau composé plusieurs AS et routeurs. À partir d'un fichier `.json` décrivant l'intention réseau, le programme :

- Génère les classes et structures de données nécessaires pour représenter les AS, routeurs et interfaces
- Crée les fichiers de configuration `.cfg` pour chaque routeur
- Place automatiquement les fichiers générés dans GNS3

## Fonctionnalités Principales

### Entrées du Projet
- **Fichier d'intention (JSON)** : Décrit l'architecture réseau
  - Définition des AS 
  - Définition des relations inter-AS (providers, peers, clients)
  - Configuration des routeurs et de leurs interfaces
  - Adresses IP, protocoles de routage (BGP, OSPF, RIP)

### Sorties du Projet
- **Fichiers de configuration `.cfg`** : Un fichier par routeur
  - Configuration complète des interfaces
  - Configuration des protocoles de routage
  - Placement automatique dans GNS3

## Structure du Projet

```
gns/
├── code/                           # Code source principal
│   ├── intent_file*.json           # Fichiers d'intention réseau
│   ├── main.py                     # Point d'entrée du programme
│   ├── router.py                   # Classe Router
│   ├── interface.py                # Classe Interface
│   ├── AS.py                       # Classe AS
│   ├── generate_classes.py         # Génération des classes à partir du JSON
│   ├── write_config.py             # Génération des fichiers .cfg
│   ├── generer_plan_adressage.py   # Génération du plan d'adressage
│   └── drag_n_drop_bot.py          # Placement automatique dans GNS3
├── Projet_test/                    # Dossier du projet GNS3
│   └── Projet_GNS.gns3             # Projet GNS3
└── 
```

## Architecture du Système

### Classes Principales

#### `Router`
```python
class Router():
    - name: str                    # Nom du routeur
    - ID: str                      # ID du routeur (ex: 1.1.1.1)
    - nb_int: int                  # Nombre d'interfaces
    - liste_int: List[Interface]   # Liste des interfaces
    - AS_name: str                 # Nom de l'AS auquel appartient le routeur
```

#### `Interface`
```python
class Interface():
    - name: str                    # Nom de l'interface (G1/0, LOOPBACK0, etc.)
    - address: str                 # Adresse IP
    - neighbors_address: List[str] # Adresses des routeurs voisin
    - protocol: str                # Protocole utilisé (BGP, OSPF, RIP)
```

#### `AS`
```python
class AS():
    - name: str                    # Numéro de l'AS
    - providers: List[AS]          # AS fournisseurs
    - peers: List[AS]              # AS pairs
    - clients: List[AS]            # AS clients
```

## Pipeline de Traitement

1. **Lecture du fichier d'intention (JSON)**
   - `json_to_dict()` : Convertit le fichier JSON en dictionnaire Python

2. **Génération des classes réseau**
   - `generate_network_classes()` : Crée les objets Router, Interface et AS
   - `generate_router()` : Crée un routeur spécifique
   - `generate_interfaces()` : Génère les interfaces d'un routeur

3. **Génération du plan d'adressage**
   - `generer_plan_adressage()` : Crée un plan d'adressage cohérent

4. **Génération des configurations**
   - `write_config()` : Génère le fichier `.cfg` pour chaque routeur
   - `write_header()` : En-tête de configuration
   - `write_interfaces_config()` : Configuration des interfaces
   - `write_bgp_config()` : Configuration BGP

5. **Placement dans GNS3**
   - `drag_and_drop()` : Place automatiquement les fichiers dans l'arborescence GNS3

## Format du Fichier d'Intention (JSON)

```json
{
    "Intent": {},
    "Structure": {
        "AS1": {
            "AS_NAME": "1111",
            "PROTOCOL": "RIP",
            "ROUTERS": {
                "R1": {
                    "ROUTER_ID": "1.1.1.1",
                    "INTERFACES": {
                        "G1/0": {
                            "ADDRESS": "1111:0:0:1::11/64",
                            "NEIGHBORS_ADDRESS": ["1111:0:0:1::12/64"]
                        }
                    }
                }
            }
        }
    }
}
```

## Utilisation

### Prérequis
- Python 3.x
- GNS3 installé et configuré

### Exécution

1. Préparez votre fichier d'intention `intent_file.json`

2. Modifiez `main.py` pour pointer vers votre fichier :
```python
FILE_NAME = "intent_file.json"
PROJECT_NAME = "nom_de_votre_projet"
```

3. Exécutez le programme :
```bash
python main.py
```

4. Les fichiers `.cfg` seront générés dans le dossier `dynamips/`

## Documentation Complémentaire

Voir [code_structure.md](code_structure.md) pour une documentation technique détaillée sur la structure du code et les étapes de développement.

## État du Projet

- Classes Router, Interface, AS
- Génération des classes à partir du JSON
- Génération des fichiers de configuration basiques
- Configuration des interfaces
- Configuration BGP (en cours de développement)
- Support complet IPv6 (en cours)
- Optimisation du drag & drop bot

## Auteurs

Robin Jenny, Léa Danober, Elie Gautier et Rémi Duran  

## Notes Importantes

- Les noms des routeurs dans l'arborescence GNS3 sont anonymes (i1, i2, i3, etc.)
- L'ordre des interfaces et des routeurs dans le fichier d'intention doit correspondre à l'ordre dans GNS3
- Vérifiez toujours les adresses IP avant de lancer la simulation
