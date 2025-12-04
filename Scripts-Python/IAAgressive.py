"""
TP Monopoly - Squelette de code
Durée: 16h sur 4 séances de 4h
"""
from typing import List, Optional

from Joueur import Joueur
from Propriete import Propriete
from StrategieIA import StrategieIA


class IAAgressive(StrategieIA):
    """Stratégie agressive: achète systématiquement toutes les propriétés"""
    
    def __init__(self):
        super().__init__("Agressive")
    
    def decider_achat(self, joueur: 'Joueur', propriete: Propriete) -> bool:
        return True

    def decider_construction(self, joueur: 'Joueur') -> Optional[Propriete]:
        """Retourne la première propriété sur laquelle l'IA agressive peut construire.

        Comportement agressif : construire dès que possible (aucune réserve minimale).
        - Si une propriété a 4 maisons et l'IA a assez pour un hôtel (5×prix_maison), la choisir.
        - Sinon, choisir la première propriété constructible pour une maison si l'IA a au moins `prix_maison`.
        - Ne considère que les quartiers complets détenus par le joueur (ou fallback couleur).
        - Retourne `None` si aucune construction possible.
        """
        from Gare import Gare
        from Compagnie import Compagnie

        for prop in joueur.proprietes:
            # ne pas construire sur gare/compagnie
            if not isinstance(prop, Propriete) or isinstance(prop, (Gare, Compagnie)):
                continue

            # Exclure hypothèques
            if getattr(prop, 'hypothequee', False):
                continue

            # Vérifier possession complète du quartier
            if getattr(prop, 'quartier', None) is not None:
                if not prop.quartier.possederQuartier(joueur):
                    continue
            else:
                if not joueur.possede_quartier_complet(prop.couleur):
                    continue

            # Si déjà hôtel, skip
            if prop.nb_maisons >= 5:
                continue

            # Prioriser promotion vers hôtel si possible
            if prop.nb_maisons == 4 and joueur.argent >= prop.prix_maison * 5 and prop.peut_construire(joueur):
                return prop

            # Sinon, construire une maison si possible
            if prop.nb_maisons < 4 and joueur.argent >= prop.prix_maison and prop.peut_construire(joueur):
                return prop

        return None

if __name__ == "__main__":
    ia = IAAgressive()
    print("OK")