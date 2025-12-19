# ==========================
# Écriture des configurations
# ==========================

from router import Router
from interface import Interface


def write_config(router, path_to_router, out_file):
    """Écrit la configuration complète d'un routeur dans un fichier .cfg."""
    pass


def write_header(router):
    """Écrit l'en-tête de la configuration du routeur."""
    pass


def write_interfaces_config(router):
    """Écrit la configuration de toutes les interfaces du routeur."""
    pass


def write_loopback(interface):
    """Écrit la configuration d'une interface loopback."""
    pass


def write_FE(interface):
    """Écrit la configuration d'une interface FastEthernet."""
    pass


def write_GE(interface):
    """Écrit la configuration d'une interface GigabitEthernet."""
    pass


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
