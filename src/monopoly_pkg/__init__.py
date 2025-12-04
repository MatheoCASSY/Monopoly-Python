"""Monopoly package - regroupement des modules.

Exporte les symboles principaux pour un import centralisé.
"""
from .game import Monopoly
from .cases import Case, Propriete, Gare, Compagnie, CaseSpeciale, TypeCase
from .joueur import Joueur
from .cartes import CarteCommunaute, PaquetCartes
from .strategies import StrategieIA, IAAgressive, IAConservative, IAStrategique
from .stats import StatistiquesPartie

__all__ = [
    'Monopoly', 'Case', 'Propriete', 'Gare', 'Compagnie', 'CaseSpeciale', 'TypeCase',
    'Joueur', 'CarteCommunaute', 'PaquetCartes', 'StrategieIA', 'IAAgressive',
    'IAConservative', 'IAStrategique', 'StatistiquesPartie'
]
