"""
TP Monopoly - Squelette de code
Durée: 16h sur 4 séances de 4h
"""
from typing import List, Optional

from Joueur import Joueur
from Propriete import Propriete
from StrategieIA import StrategieIA

class IAConservative(StrategieIA):
    """Stratégie conservative: n'achète que si garde une réserve"""
    
    def __init__(self):
        super().__init__("Conservative")
    
    def decider_achat(self, joueur: 'Joueur', propriete: Propriete) -> bool:
        """Achète seulement si argent > 2x le prix"""
        return joueur.argent >= propriete.prix * 2
    
    def decider_construction(self, joueur: 'Joueur') -> Optional[Propriete]:
        """
        Retourne une propriété sur laquelle construire si:
        - le joueur possède le quartier complet
        - la propriété peut être construite
        - le joueur a au moins 2x le coût d'achat (maison ou hôtel)

        La méthode est appelée en boucle par le moteur, donc tant que
        l'IA peut construire et a assez d'argent, elle continuera.
        """
        # Récupérer les propriétés constructibles du joueur
        candidates: List[Propriete] = []
        for prop in joueur.proprietes:
            if not isinstance(prop, Propriete):
                continue
            # Vérifier possession du quartier
            possede = False
            if getattr(prop, 'quartier', None) is not None:
                try:
                    possede = prop.quartier.possederQuartier(joueur)
                except Exception:
                    possede = False
            else:
                try:
                    possede = joueur.possede_quartier_complet(prop.couleur)
                except Exception:
                    possede = False

            if not possede:
                continue

            # Vérifier si construction possible (répartition respectée)
            if not prop.peut_construire(joueur):
                continue

            # Calculer le coût nécessaire: maison ou hôtel
            if prop.nb_maisons < 4:
                cout = prop.prix_maison
            elif prop.nb_maisons == 4:
                cout = prop.prix_maison * 5
            else:
                # Déjà hôtel
                continue

            # Condition conservative: le joueur doit avoir au moins 2x le coût
            if joueur.argent >= cout * 2:
                candidates.append(prop)

        if not candidates:
            return None

        # Choisir la propriété la plus 'nécessaire' (moins de maisons d'abord)
        candidates.sort(key=lambda p: (p.nb_maisons, -p.prix_maison))
        return candidates[0]