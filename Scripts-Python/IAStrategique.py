"""
TP Monopoly - Squelette de code
Durée: 16h sur 4 séances de 4h
"""
from typing import List, Optional

from Joueur import Joueur
from Propriete import Propriete
from StrategieIA import StrategieIA

class IAStrategique(StrategieIA):
    """Stratégie stratégique: privilégie les quartiers"""
    
    def __init__(self):
        super().__init__("Stratégique")
    
    def decider_achat(self, joueur: 'Joueur', propriete: Propriete) -> bool:
        """Privilégie les propriétés qui complètent un quartier"""
        # Ne pas dépenser si trop peu d'argent
        if joueur.argent < propriete.prix * 1.5:
            return False
        # Si la propriété appartient à un objet Quartier, compter les propriétés du quartier possédées
        nb_possede = 0
        if getattr(propriete, 'quartier', None) is not None:
            nb_possede = sum(1 for p in propriete.quartier.proprietes if p.proprietaire == joueur)
        else:
            # fallback : compter par couleur
            nb_possede = sum(1 for p in joueur.proprietes if hasattr(p, 'couleur') and p.couleur == propriete.couleur)

        # Haute priorité si ça rapproche d'un quartier
        if nb_possede >= 1:
            return True
        
        # Sinon acheter si beaucoup d'argent
        return joueur.argent >= propriete.prix * 3

    def decider_construction(self, joueur: 'Joueur') -> Optional[Propriete]:
        """Choisit la meilleure propriété sur laquelle construire.

        Règles :
        - Ne considère que les quartiers complets détenus par le joueur.
        - Ne propose que des propriétés constructibles (pas gare/compagnie, pas hypothéquées).
        - Priorise les propriétés avec le moins de maisons (répartition équilibrée),
          puis par `prix_maison` décroissant pour maximiser l'impact.
        - Retourne la `Propriete` choisie ou `None` si aucune construction n'est souhaitable.
        """
        # Rassembler les propriétés constructibles dans des quartiers complets
        candidats: List[Propriete] = []
        for prop in joueur.proprietes:
            from Gare import Gare
            from Compagnie import Compagnie

            if not isinstance(prop, Propriete) or isinstance(prop, (Gare, Compagnie)):
                continue

            # Vérifier que le joueur possède le quartier complet
            couleur = prop.quartier.couleur if getattr(prop, 'quartier', None) is not None else prop.couleur
            possede = False
            if getattr(prop, 'quartier', None) is not None:
                possede = prop.quartier.possederQuartier(joueur)
            else:
                possede = joueur.possede_quartier_complet(couleur)

            if not possede:
                continue

            # Exclure propriétés hypothéquées ou déjà à l'hôtel
            if getattr(prop, 'hypothequee', False):
                continue
            if prop.nb_maisons >= 5:
                continue

            # Vérifier que la propriété permet la construction selon les règles
            if not prop.peut_construire(joueur):
                continue

            candidats.append(prop)

        if not candidats:
            return None

        # Trier: d'abord par nombre de maisons (asc), puis par prix_maison (desc)
        candidats.sort(key=lambda p: (p.nb_maisons, - (getattr(p, 'prix_maison', 0))))

        # Choisir le meilleur candidat
        return candidats[0]