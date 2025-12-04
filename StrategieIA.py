"""
TP Monopoly - Squelette de code
Durée: 16h sur 4 séances de 4h
"""
from typing import List, Optional

from Propriete import Propriete
from abc import *

class StrategieIA(ABC) :
    """Classe de base pour les stratégies d'intelligence artificielle"""
    
    def __init__(self, nom: str):
        self.nom = nom
    
    @abstractmethod
    def decider_achat(self, joueur: 'Joueur', propriete: Propriete) -> bool:
        """Décide si l'IA doit acheter une propriété"""
        pass
    
    @abstractmethod
    def decider_construction(self, joueur: 'Joueur') -> Optional[Propriete]:
        """Décide sur quelle propriété construire"""
        pass
    
