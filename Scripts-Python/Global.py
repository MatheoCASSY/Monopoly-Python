
from enum import Enum

# =============================================================================
# ÉNUMÉRATIONS ET CONSTANTES
# =============================================================================

class TypeCase(Enum):
    """Types de cases spéciales"""
    DEPART = "depart"
    PRISON = "prison"
    PARC_GRATUIT = "parc_gratuit"
    ALLER_PRISON = "aller_prison"
    TAXE = "taxe"
    CHANCE = "chance"
    CAISSE_COMMUNAUTE = "caisse"

# Constantes du jeu
ARGENT_INITIAL = 1500
ARGENT_PASSAGE_DEPART = 200
ARGENT_ARRET_DEPART = 400
PRIX_SORTIE_PRISON = 50
NOMBRE_CASES = 40