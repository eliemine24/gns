import ipaddress
import json
import copy

import ipaddress
import json

def generer_plan(data):
    # 1. Configuration des bases
    prefixes = {
        "AS1": ipaddress.IPv6Network("1111::/48"),
        "AS2": ipaddress.IPv6Network("2222::/48"),
        "INTER_AS": ipaddress.IPv6Network("3333::/64")
    }
    
    # Registre pour stocker les IPs : { "R1": { "G1/0": "IP", "LB": "IP" } }
    registre_ips = {}
    as_mapping = {} # Pour savoir quel routeur appartient à quelle AS
    
    # --- PREMIER PASSAGE : ATTRIBUTION ---
    # On isole les liens pour ne pas les traiter deux fois
    liens_vus = set()
    idx_lien = {"AS1": 1, "AS2": 1}

    for as_id, as_content in data["Structure"].items():
        for r_name, r_content in as_content["ROUTERS"].items():
            registre_ips[r_name] = {}
            as_mapping[r_name] = as_id
            
            # Loopback : Format 1111:0:0:3::11X
            r_num = int(''.join(filter(str.isdigit, r_name)))
            lb_ip = str(prefixes[as_id][0]).replace('::', f':3::11{r_num}')
            registre_ips[r_name]["LOOPBACK0"] = f"{lb_ip}/128"

            for int_name, int_content in r_content["INTERFACES"].items():
                neighbor_name = list(int_content["NEIGHBORS"].keys())[0]
                pair = tuple(sorted((r_name, neighbor_name)))
                
                if pair not in liens_vus:
                    if int_content.get("PROTOCOL") == "EBGP":
                        # EBGP : 3333::31 et 3333::32
                        liens_vus.add((pair, "3333::31/64", "3333::32/64"))
                    else:
                        # Interne : on utilise l'index de lien
                        sub = list(prefixes[as_id].subnets(new_prefix=64))[idx_lien[as_id]]
                        idx_lien[as_id] += 1
                        liens_vus.add((pair, f"{sub[11]}/64", f"{sub[12]}/64")) # Format ::b et ::c
                
    # On remplit le registre à partir des liens vus
    for (node_a, node_b), ip_a, ip_b in liens_vus:
        # On retrouve quelle interface de node_a va vers node_b
        for r in [node_a, node_b]:
            target = node_b if r == node_a else node_a
            my_ip = ip_a if r == node_a else ip_b
            for int_name, int_info in data["Structure"][as_mapping[r]]["ROUTERS"][r]["INTERFACES"].items():
                if list(int_info["NEIGHBORS"].keys())[0] == target:
                    registre_ips[r][int_name] = my_ip

    # --- SECOND PASSAGE : CONSTRUCTION DU JSON FINAL ---
    resultat = {"Intent": {}, "Structure": {}}
    
    for as_id, as_content in data["Structure"].items():
        resultat["Structure"][as_id] = {
            "AS_NAME": as_content["AS_NAME"],
            "PROTOCOL": as_content["PROTOCOL"],
            "ROUTERS": {}
        }
        
        routers_in_as = list(as_content["ROUTERS"].keys())
        
        for r_name, r_content in as_content["ROUTERS"].items():
            r_num = int(''.join(filter(str.isdigit, r_name)))
            res_router = {
                "ROUTER_ID": f"{r_num}.{r_num}.{r_num}.{r_num}",
                "INTERFACES": {}
            }
            
            # Interfaces physiques
            for int_name, int_info in r_content["INTERFACES"].items():
                neighbor = list(int_info["NEIGHBORS"].keys())[0]
                neighbor_int = int_info["NEIGHBORS"][neighbor]
                
                res_router["INTERFACES"][int_name] = {
                    "ADDRESS": registre_ips[r_name][int_name],
                    "NEIGHBORS_ADDRESS": [registre_ips[neighbor][neighbor_int]]
                }
                if "PROTOCOL" in int_info: res_router["INTERFACES"][int_name]["PROTOCOL"] = "EBGP"
                if "COST" in int_info: res_router["INTERFACES"][int_name]["COST"] = int_info["COST"]

            # Loopback
            others_lb = [registre_ips[other]["LOOPBACK0"] for other in routers_in_as if other != r_name]
            res_router["INTERFACES"]["LOOPBACK0"] = {
                "ADDRESS": registre_ips[r_name]["LOOPBACK0"],
                "NEIGHBORS_ADDRESS": others_lb
            }
            
            resultat["Structure"][as_id]["ROUTERS"][r_name] = res_router

    return resultat


# --- Lancement ---
intention_json = {
    "Intent":{

    },
    "Structure":{

        "AS1":{

            "AS_NAME" : "1111",
            "PROTOCOL": "RIP",

            "ROUTERS":{
                
                "R1":{

                    "INTERFACES":{

                        "G1/0": {
                            "NEIGHBORS": {"R2": "G1/0"}
                        }
                    }
                },
                
                "R2":{
                    
                    "INTERFACES":{

                        "G1/0": {
                            "NEIGHBORS":{"R1":"G1/0"}
                        },

                        "G2/0": {
                            "NEIGHBORS":{"R3":"G2/0"}
                        }
                    }
                },
                
                "R3":{
                    
                    "INTERFACES":{

                        "G1/0": {
                            "NEIGHBORS":{"R4":"G1/0"},
                            "PROTOCOL": "EBGP"
                        },

                        "G2/0": {
                            "NEIGHBORS":{"R2":"G2/0"}
                        }
                    }
                }
            }
        },
        "AS2":{

            "AS_NAME" : "2222",
            "PROTOCOL": "OSPF",

            "ROUTERS":{
                
                "R4":{
                    
                    "INTERFACES":{

                        "G1/0": {
                            "NEIGHBORS":{"R3":"G1/0"},
                            "PROTOCOL": "EBGP"
                        },

                        "G2/0": {
                            "NEIGHBORS":{"R5":"G2/0"},
                            "COST":100
                        }
                    }
                },
                
                "R5":{

                    "INTERFACES":{

                        "G1/0": {
                            "NEIGHBORS":{"R6":"G1/0"},
                            "COST":100
                        },

                        "G2/0": {
                            "NEIGHBORS":{"R4":"G2/0"},
                            "COST":100
                        }
                    }
                },
                
                "R6":{

                    "INTERFACES":{

                        "G1/0": {
                            "NEIGHBORS":{"R5":"G1/0"},
                            "COST":100
                        }
                    }
                }
            }
        }
    }
}

# (Remplace par ton dictionnaire complet)
mon_plan = generer_plan(intention_json)
print(json.dumps(mon_plan, indent=4))


