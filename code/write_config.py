# ==========================
# Écriture des configurations
# ==========================

from router import Router
from interface import Interface
from datetime import datetime


def write_config(router, path_to_router, out_file):
    """Écrit la configuration complète d'un routeur dans un fichier .cfg."""
    conf = open(out_file, 'x')
    write_header(conf, router)
    write_interfaces_config(conf, router)
    #write_bgp_config(conf, router)
    #write_ipv4_address_family(conf, router)
    #write_ipv6_address_family(conf, router)
    conf.close()
    return out_file


def write_header(conf, router):
    """Écrit l'en-tête de la configuration du routeur."""
    date = datetime.now().strftime('%I:%M:%S UTC %a %b %d %Y')
    conf.write("""!
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
!""")


def write_interfaces_config(conf, router):
    """Écrit la configuration de toutes les interfaces du routeur."""
    for interface in router.liste_int:
        if 'Loopback' in interface:
            write_loopback(interface)
        elif 'FastEthernet' in interface:
            write_FE(interface)
        else:
            write_GE(interface)


def write_loopback(conf, interface):
    """Écrit la configuration d'une interface loopback."""
    conf.write("""interface {interface}
no ip address
ipv6 address {interface.address}
ipv6 enable""")
    if interface.protocol == 'ospf':
        conf.write("""ipv6 ospf 10 area 1""")
    conf.write("""!""")


def write_FE(conf, interface):
    """Écrit la configuration d'une interface FastEthernet."""
    conf.write("""interface {interface}
no ip address
shutdown
duplex full
!""")


def write_GE(conf, interface):
    """Écrit la configuration d'une interface GigabitEthernet."""
    conf.write("""interface {interface}
no ip address
negotiation auto""")
    for add in interface.neighbors_address:
        conf.write("""ipv6 address {add}""")
    conf.write("""ipv6 enable
!""")


# ==========================
# Protocoles de routage
# ==========================

def write_bgp_config(router):
    """Écrit la configuration BGP du routeur."""
    pass


def write_ipv4_address_family(router):
    """Écrit la configuration address-family IPv4."""
    pass


def write_ipv6_address_family(router):
    """Écrit la configuration address-family IPv6."""
    pass


# ==========================
# Intégration GNS
# ==========================

def drag_and_drop_bot(cfg_file, out_path):
    """Place le fichier .cfg généré dans l'arborescence GNS."""
    pass