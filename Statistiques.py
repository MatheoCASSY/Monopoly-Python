"""
TP Monopoly - Squelette de code
Durée: 16h sur 4 séances de 4h
"""
from typing import Dict, Optional



class StatistiquesPartie :
    """Collecte et analyse des statistiques d'une partie"""
    
    def __init__(self):
        self.passages_par_case: Dict[int, int] = {}
        self.revenus_par_propriete: Dict[str, int] = {}
        self.nb_tours = 0
        self.gagnant: Optional[Joueur] = None
    
    def enregistrer_passage(self, case: 'Case'):
        """Enregistre le passage d'un joueur sur une case"""
        pos = case.position
        if pos not in self.passages_par_case:
            """ premier passage """
            self.passages_par_case[pos] = 1
        else:
            self.passages_par_case[pos] += 1
    
    def enregistrer_loyer(self, propriete: 'Propriete', montant: int):
        """Enregistre un paiement de loyer"""
        nom = propriete.nom
        if nom not in self.revenus_par_propriete:
            """ premier loyer  """
            self.revenus_par_propriete[nom] = montant
        else:
            self.revenus_par_propriete[nom] += montant
    
    def afficher_statistiques(self):
        """Affiche un résumé des statistiques"""
        print("\n" + "="*60)
        print("STATISTIQUES DE LA PARTIE")
        print("="*60)
        
        print(f"\nDurée: {self.nb_tours} tours")
        if self.gagnant:
            print(f"Gagnant: {self.gagnant.nom} avec {self.gagnant.argent}€")
        
        # Top 5 des cases les plus visitées
        if self.passages_par_case:
            print("\nTop 5 des cases les plus visitées:")
            top_cases = sorted(self.passages_par_case.items(), 
                              key=lambda x: x[1], reverse=True)[:5]
            for position, nb in top_cases:
                proba = (nb / sum(self.passages_par_case.values())) * 100
                print(f"   Position {position:2}: {nb:3} passages ({proba:.1f}%)")
        
        # Top 5 des propriétés les plus rentables
        if self.revenus_par_propriete:
            print("\nTop 5 des propriétés les plus rentables:")
            top_proprietes = sorted(self.revenus_par_propriete.items(), 
                                   key=lambda x: x[1], reverse=True)[:5]
            for nom, revenus in top_proprietes:
                print(f"   {nom:30}: {revenus:4}€ de loyers")
