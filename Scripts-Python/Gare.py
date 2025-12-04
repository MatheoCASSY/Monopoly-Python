"""
TP Monopoly - Squelette de code
Durée: 16h sur 4 séances de 4h
"""

from Propriete import Propriete

class Gare(Propriete):
    """Case représentant une gare"""
    
    def __init__(self, nom: str, position: int):
        super().__init__(nom, position, prix=200, loyer=25, couleur="gare", prix_maison=0)
    
    def calculer_loyer(self) -> int:
        """Le loyer dépend du nombre de gares possédées"""
        if self.hypothequee or not self.proprietaire:
            return 0
        
        nb_gares = sum(1 for p in self.proprietaire.proprietes 
                      if isinstance(p, Gare))
        
        loyers = {1: 25, 2: 50, 3: 100, 4: 200}
        return loyers.get(nb_gares, 25)
    
    def peut_construire(self, joueur: 'Joueur') -> bool:
        """Pas de construction sur les gares"""
        return False