"""
TP Monopoly - Squelette de code
Durée: 16h sur 4 séances de 4h
"""

from Propriete import Propriete
from Case import Case
from CaseSpeciale import CaseSpeciale
from Gare import Gare
from Compagnie import Compagnie 

from Global import TypeCase

from typing import List, Optional

from db import DB

class Plateau:
    """Représente le plateau de jeu Monopoly"""
    def __init__(self):
        self.cases: List['Case'] = [] # type: ignore
        self._creer_plateau()
    
    def _creer_plateau(self):
        """Crée les 40 cases du plateau Monopoly"""
        # TODO SÉANCE 1: Créer les cases du plateau
        # Version simplifiée pour démarrer:
       
        for p in DB.get_proprietes():
            self.cases.append(p)

       # Position 0: Départ
        self.cases.append(CaseSpeciale("Départ", 0, TypeCase.DEPART, 200))
        
        
        # Positions 1-9: Propriétés marron et bleu clair
        #self.cases.append(Propriete("Boulevard de Belleville", 1, 60, 2, "marron", 50))
        self.cases.append(CaseSpeciale("Caisse de Communauté", 2, TypeCase.CAISSE_COMMUNAUTE))
        #self.cases.append(Propriete("Rue Lecourbe", 3, 60, 4, "marron", 50))
        self.cases.append(CaseSpeciale("Impôts sur le revenu", 4, TypeCase.TAXE, 200))
        #self.cases.append(Gare("Gare Montparnasse", 5))
        #self.cases.append(Propriete("Rue de Vaugirard", 6, 100, 6, "bleu_clair", 50))
        self.cases.append(CaseSpeciale("Chance", 7, TypeCase.CHANCE))
        #self.cases.append(Propriete("Rue de Courcelles", 8, 100, 6, "bleu_clair", 50))
        #self.cases.append(Propriete("Avenue de la République", 9, 120, 8, "bleu_clair", 50))
        
        # Position 10: Prison (simple visite)
        self.cases.append(CaseSpeciale("Prison / Simple visite", 10, TypeCase.PRISON))
        
        # Positions 11-19: Propriétés roses
        #self.cases.append(Propriete("Boulevard de la Villette", 11, 140, 10, "rose", 100))
        #self.cases.append(Compagnie("Compagnie d'Électricité", 12))
        #self.cases.append(Propriete("Avenue de Neuilly", 13, 140, 10, "rose", 100))
        #self.cases.append(Propriete("Rue de Paradis", 14, 160, 12, "rose", 100))
        #self.cases.append(Gare("Gare de Lyon", 15))
        #self.cases.append(Propriete("Avenue Mozart", 16, 180, 14, "orange", 100))
        self.cases.append(CaseSpeciale("Caisse de Communauté", 17, TypeCase.CAISSE_COMMUNAUTE))
        #self.cases.append(Propriete("Boulevard Saint-Michel", 18, 180, 14, "orange", 100))
        #self.cases.append(Propriete("Place Pigalle", 19, 200, 16, "orange", 100))
        # Position 20: Parc Gratuit
        self.cases.append(CaseSpeciale("Parc Gratuit", 20, TypeCase.PARC_GRATUIT))
        
        # Positions 21-29: Propriétés rouges et jaunes
        #self.cases.append(Propriete("Avenue Matignon", 21, 220, 18, "rouge", 150))
        self.cases.append(CaseSpeciale("Chance", 22, TypeCase.CHANCE))
        #self.cases.append(Propriete("Boulevard Malesherbes", 23, 220, 18, "rouge", 150))
        #self.cases.append(Propriete("Avenue Henri-Martin", 24, 240, 20, "rouge", 150))
        #self.cases.append(Gare("Gare du Nord", 25))
        #self.cases.append(Propriete("Faubourg Saint-Honoré", 26, 260, 22, "jaune", 150))
        #self.cases.append(Propriete("Place de la Bourse", 27, 260, 22, "jaune", 150))
        #self.cases.append(Compagnie("Compagnie des Eaux", 28))
        #self.cases.append(Propriete("Rue La Fayette", 29, 280, 24, "jaune", 150))
        
        # Position 30: Aller en prison
        self.cases.append(CaseSpeciale("Allez en prison", 30, TypeCase.ALLER_PRISON))
        
        # Positions 31-39: Propriétés vertes et bleues foncées
        #self.cases.append(Propriete("Avenue de Breteuil", 31, 300, 26, "vert", 200))
        #self.cases.append(Propriete("Avenue Foch", 32, 300, 26, "vert", 200))
        self.cases.append(CaseSpeciale("Caisse de Communauté", 33, TypeCase.CAISSE_COMMUNAUTE))
        #self.cases.append(Propriete("Boulevard des Capucines", 34, 320, 28, "vert", 200))
        #self.cases.append(Gare("Gare Saint-Lazare", 35))
        self.cases.append(CaseSpeciale("Chance", 36, TypeCase.CHANCE))
        #self.cases.append(Propriete("Avenue des Champs-Élysées", 37, 350, 35, "bleu_fonce", 200))
        self.cases.append(CaseSpeciale("Taxe de luxe", 38, TypeCase.TAXE, 100))
        #self.cases.append(Propriete("Rue de la Paix", 39, 400, 50, "bleu_fonce", 200))
    
        self.cases.sort(key=lambda x: x.position)
    
    def get_case(self, position: int) -> Case:
        """Retourne la case à une position donnée"""
        return self.cases[position % len(self.cases)]
    
    def afficher_plateau(self):
        """Affiche un résumé du plateau"""
        print("\n" + "="*60)
        print("PLATEAU DE MONOPOLY")
        print("="*60)
        for case in self.cases:
            print(f"{case.position:2}. {case.nom}")

    
if __name__ == "__main__":
    # Test basique
    plateau = Plateau()
    assert len(plateau.cases) == 40, "Le plateau doit avoir 40 cases"
    assert isinstance(plateau.cases[0], CaseSpeciale), "La case 0 est la case de départ"
    assert isinstance(plateau.cases[5], Gare), "La case 5 est une gare"
    assert plateau.cases[39].nom == "Rue de la Paix", "La case 39 est Rue de la Paix"