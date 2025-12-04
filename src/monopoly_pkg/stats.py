from typing import Dict
from .cases import Case, Propriete


class StatistiquesPartie:
    def __init__(self):
        self.passages_par_case: Dict[str, int] = {}
        self.revenus_par_propriete: Dict[str, int] = {}
        self.duree_partie = 0

    def enregistrer_passage(self, case: Case):
        key = getattr(case, 'nom', str(case))
        self.passages_par_case[key] = self.passages_par_case.get(key, 0) + 1

    def enregistrer_loyer(self, propriete: Propriete, montant: int):
        nom = getattr(propriete, 'nom', 'inconnue')
        self.revenus_par_propriete[nom] = self.revenus_par_propriete.get(nom, 0) + montant

    def afficher_statistiques(self):
        print("\n--- Statistiques de la partie ---")
        print(f"Durée (tours simulés): {self.duree_partie}")
        if self.passages_par_case:
            top = sorted(self.passages_par_case.items(), key=lambda x: x[1], reverse=True)[:5]
            print("Top 5 cases visitées:")
            for nom, cnt in top:
                print(f" - {nom}: {cnt} passages")
        else:
            print("Aucun passage enregistré.")
