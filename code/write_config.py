# ==========================
# Écriture des configurations
# ==========================

from router import Router
from interface import Interface
from datetime import datetime


def write_config(router, out_file,router_list):
    """Écrit la configuration complète d'un routeur dans un fichier .cfg."""
    conf = open(out_file, 'w')
    write_header(conf, router)
    write_interfaces_config(conf, router)
    write_bgp_config(conf, router,router_list)
    write_ipv4_address_family(conf)
    write_ipv6_address_family(conf, router)
    write_end(conf, router)
    conf.close()
    return out_file


def write_header(conf, router):
    """Écrit l'en-tête de la configuration du routeur."""
    date = datetime.now().strftime('%I:%M:%S UTC %a %b %d %Y')
    conf.write(f"""!
! Last configuration change at {date}
!
version 15.2
service timestamps debug datetime msec
service timestamps log datetime msec
!
hostname {router.name}
!
boot-start-marker
boot-end-marker
!
!
!
no aaa new-model
no ip icmp rate-limit unreachable
ip cef
!
!
!
!
!
!
no ip domain lookup
ipv6 unicast-routing
ipv6 cef
!
!
multilink bundle-name authenticated
!
!
!
!
!
!
!
!
!
ip tcp synwait-time 5
! 
!
!
!
!
!
!
!
!
!
!
!
""")

def write_end(conf, router):
    conf.write("""ip forward-protocol nd
!
!
no ip http server
no ip http secure-server
!\n""")
    protocol = "OSPF"
    for int in router.liste_int:
        if "RIP" in int.protocol_list:
            protocol = "RIP"
    if protocol == "RIP":
        conf.write("""ipv6 router rip maison
 redistribute connected\n""")
    else: 
        conf.write(f"""ipv6 router ospf 10
 router-id {router.ID}\n""")
    conf.write("""!
!
!
!
control-plane
!
!
line con 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line aux 0
 exec-timeout 0 0
 privilege level 15
 logging synchronous
 stopbits 1
line vty 0 4
 login
!
!
end\n""")

# =============================
# ======== Interfaces =========
# =============================

def write_interfaces_config(conf, router):
    """Écrit la configuration de toutes les interfaces du routeur."""
    for interface in router.liste_int:
        if interface.name == 'LOOPBACK0':
            write_loopback0(conf, interface)
        elif 'G' in interface.name :
            write_GE(conf, interface)
        else:
            write_FE(conf, interface)


def write_loopback0(conf, interface):
    """Écrit la configuration d'une interface loopback0."""
    conf.write(f"""interface {interface.name}
 no ip address
 ipv6 address {interface.address}
 ipv6 enable
""")
    if "OSPF" in interface.protocol_list :
        conf.write(""" ipv6 ospf 10 area 1\n""")
    elif "RIP" in interface.protocol_list:
        conf.write(""" ipv6 rip maison enable\n""")
    conf.write("""!\n""")


def write_FE(conf, interface):
    """Écrit la configuration d'une interface FastEthernet."""
    conf.write(f"""interface {interface.name}
 no ip address
 negotiation auto
 duplex full
!
""")
    conf.write(""" ipv6 enable
""")
    conf.write(f""" ipv6 address {interface.address}\n""")
    if "OSPF" in interface.protocol_list :
        conf.write(""" ipv6 ospf 10 area 1\n""")
    elif "RIP" in interface.protocol_list:
        conf.write(""" ipv6 rip maison enable\n""")
    conf.write(f"""!\n""")


def write_GE(conf, interface):
    """Écrit la configuration d'une interface GigabitEthernet."""
    conf.write(f"""interface {interface.name}
 no ip address
 negotiation auto
""")
    conf.write(""" ipv6 enable
""")
    conf.write(f""" ipv6 address {interface.address}\n""")
    if "OSPF" in interface.protocol_list :
        conf.write(""" ipv6 ospf 10 area 1\n""")
    elif "RIP" in interface.protocol_list:
        conf.write(""" ipv6 rip maison enable\n""")
    conf.write(f"""!\n""")


# =============================
# === Protocoles de routage ===
# =============================

def write_bgp_config(conf, router,router_list):
    """Écrit la configuration BGP du routeur."""
    conf.write(f"""!
router bgp {router.AS_name}
 bgp router-id {router.ID}
 bgp log-neighbor-changes
 no bgp default ipv4-unicast
""")
    for interface in router.liste_int:
        if interface.name == "LOOPBACK0":
            for neighbor in interface.neighbors_address:
                conf.write(f""" neighbor {neighbor.split('/', 1)[0]} remote-as {router.AS_name}
 neighbor {neighbor.split('/', 1)[0]} update-source {interface.name}
""")
        else:
            for protocol in interface.protocol_list:
                
                if protocol == "EBGP":
                    
                    #va chercher l'as-name du routeur voisin
                    for router_temp in router_list:
                        for temp_interface in router_temp.liste_int:
                            if temp_interface.address in interface.neighbors_address:
                                conf.write(f""" neighbor {temp_interface.address.split('/', 1)[0]} remote-as {router_temp.AS_name}
""")
    conf.write(f""" !\n""")

def write_ipv4_address_family(conf):
    """Écrit la configuration address-family IPv4."""
    conf.write(""" address-family ipv4
 exit-address-family
 !\n""")


def write_ipv6_address_family(conf, router):
    """Écrit la configuration address-family IPv6."""
    conf.write(""" address-family ipv6\n""")
    liste_neighbor_add = []     #łiste pour éviter les doublons
    ebgp_present = False
    for interface in router.liste_int:
        if "EBGP" in interface.protocol_list:
            ebgp_present = True
    for interface in router.liste_int:
        if "EBGP" in interface.protocol_list or interface.name == "LOOPBACK0":
            for neighbor in interface.neighbors_address:
                if neighbor not in liste_neighbor_add:
                    #(garder seulement l'addresse sans le mask)
                    conf.write(f"""  neighbor {neighbor.split('/', 1)[0]} activate\n""")
                    #si on a un protocol EBGP sur cette interface, on n'active pas next-hop-self
                    if ebgp_present and interface.name == "LOOPBACK0":
                        conf.write(f"""  neighbor {neighbor.split('/', 1)[0]} next-hop-self\n""")
    conf.write(""" exit-address-family
!\n""")
