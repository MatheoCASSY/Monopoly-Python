"""
TP Monopoly - Squelette de code
Durée: 16h sur 4 séances de 4h
"""

from Propriete import Propriete

class Compagnie(Propriete):
    """Case représentant une compagnie publique (Électricité, Eau)"""
    
    def __init__(self, nom: str, position: int):
        super().__init__(nom, position, prix=150, loyer=0, couleur="compagnie", prix_maison=0)
        self.dernier_lancer_des = 0
    
    def calculer_loyer(self) -> int:
        """Le loyer dépend du lancer de dés et du nombre de compagnies"""
        if self.hypothequee or not self.proprietaire:
            return 0
        
        nb_compagnies = sum(1 for p in self.proprietaire.proprietes 
                         if isinstance(p, Compagnie))
        
        multiplicateur = 4 if nb_compagnies == 1 else 10
        return multiplicateur * self.dernier_lancer_des
    
    def action(self, joueur: 'Joueur', jeu: 'Monopoly'):
        """Avant de calculer le loyer, on stocke le lancer de dés"""
        self.dernier_lancer_des = jeu.dernier_total_des
        super().action(joueur, jeu)
    
    def peut_construire(self, joueur: 'Joueur') -> bool:
        """Pas de construction sur les compagnies"""
        return False
