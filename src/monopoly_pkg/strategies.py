from typing import List, Optional

from .joueur import Joueur
from .cases import Propriete


class StrategieIA:
    def decider_achat(self, joueur: Joueur, propriete: Propriete) -> bool:
        try:
            if propriete.prix <= 200 and joueur.argent >= propriete.prix * 1.5:
                return True
        except Exception:
            pass
        return False

    def decider_construction(self, joueur: Joueur, proprietes_quartier: List[Propriete]) -> Optional[Propriete]:
        for p in proprietes_quartier:
            if joueur.peut_construire_maison(p):
                return p
        return None


class IAAgressive(StrategieIA):
    def __init__(self):
        self.nom = "Agressive"

    def decider_achat(self, joueur: Joueur, propriete: Propriete) -> bool:
        return joueur.argent >= propriete.prix


class IAConservative(StrategieIA):
    def __init__(self):
        self.nom = "Conservative"

    def decider_achat(self, joueur: Joueur, propriete: Propriete) -> bool:
        return joueur.argent > 2 * propriete.prix


class IAStrategique(StrategieIA):
    def __init__(self):
        self.nom = "Strategique"

    def decider_achat(self, joueur: Joueur, propriete: Propriete) -> bool:
        if joueur.argent < 1.5 * propriete.prix:
            return False
        nb_possede = sum(1 for p in joueur.proprietes if hasattr(p, 'couleur') and p.couleur == propriete.couleur)
        nb_par_couleur = {
            "marron": 2, "bleu_clair": 3, "rose": 3, "orange": 3,
            "rouge": 3, "jaune": 3, "vert": 3, "bleu_fonce": 2
        }
        req = nb_par_couleur.get(propriete.couleur, None)
        if req is not None and nb_possede + 1 >= req:
            return True
        if joueur.argent >= 3 * propriete.prix:
            return True
        return False

    def decider_construction(self, joueur: Joueur, proprietes_quartier: List[Propriete]) -> Optional[Propriete]:
        meilleure = None
        meilleur_roi = 0.0
        for prop in proprietes_quartier:
            if not joueur.peut_construire_maison(prop):
                continue
            try:
                loyer_actuel = prop.calculer_loyer()
                prop.nb_maisons += 1
                loyer_futur = prop.calculer_loyer()
                prop.nb_maisons -= 1
                prix_maison = getattr(prop, 'prix_maison', prop.prix // 2)
                if prix_maison <= 0:
                    continue
                roi = (loyer_futur - loyer_actuel) / prix_maison
                if roi > meilleur_roi:
                    meilleur_roi = roi
                    meilleure = prop
            except Exception:
                continue
        return meilleure
