"""
TP Monopoly - Squelette de code
Durée: 16h sur 4 séances de 4h
"""
from Case import Case

from typing import Optional

class Propriete(Case):
    """Case représentant une propriété achetable"""
    def __init__(self, nom: str, position: int, prix: int, loyer: int, couleur: str, prix_maison: int = 50):
        super().__init__(nom, position)
        self.prix = prix
        self.loyer_base = loyer
        self.couleur = couleur
        self.proprietaire: Optional['Joueur'] = None # type: ignore
        self.nb_maisons = 0
        self.a_hotel = False
        self.prix_maison = prix_maison
        self.hypothequee = False
    
    def calculer_loyer(self) -> int:
        """Calcule le loyer en fonction des maisons/hôtels"""
        if self.hypothequee or not self.proprietaire:
            return 0
        
        if self.a_hotel:
            return self.loyer_base * 100
        elif self.nb_maisons > 0:
            # Multiplicateurs: 1 maison=×5, 2=×15, 3=×45, 4=×80
            multiplicateurs = [5, 15, 45, 80]
            return self.loyer_base * multiplicateurs[self.nb_maisons - 1]
        elif self.proprietaire.possede_quartier_complet(self.couleur):
            # Quartier sans construction = loyer double
            return self.loyer_base * 2
        else:
            return self.loyer_base
    

    def peut_construire(self, joueur: 'Joueur') -> bool:
        """Vérifie si on peut construire sur cette propriété"""
        if self.proprietaire != joueur:
            return False
        
        if joueur.est_en_faillite:
            return False
        
        if joueur.argent < self.prix_maison:
            return False
        
        if not joueur.possede_quartier_complet(self.couleur):
            return False
          
        if self.hypothequee:
            return False
        
        if self.a_hotel:
            return False
        
        nbMaisonsMin = min([p.nb_maisons for p in joueur.proprietes])
        if self.nb_maisons > nbMaisonsMin:
             return False
        
        # ici ok
        return True
    
    def construire_maison(self, joueur: 'Joueur') -> bool:
        """Construit une maison (maximum 4)"""
        if not self.peut_construire(joueur):
            return False
        
        if self.nb_maisons >= 4:
            return False
        
        if joueur.argent < self.prix_maison:
            return False
        
        joueur.payer(self.prix_maison)
        self.nb_maisons += 1
        return True
    
    def construire_hotel(self, joueur: 'Joueur') -> bool:
        """Construit un hôtel (nécessite 4 maisons)"""
        if not self.peut_construire(joueur):
            return False
        
        if self.nb_maisons != 4:
            return False
        
        if joueur.argent < self.prix_maison:
            return False
        
        joueur.payer(self.prix_maison)
        self.nb_maisons = 0
        self.a_hotel = True
        return True
   
    def action(self, joueur: 'Joueur', jeu: 'Monopoly'):
        """Gère l'arrivée d'un joueur sur la propriété"""
        if self.proprietaire is None:
            # Propriété libre - proposer l'achat
            if joueur.argent >= self.prix:
                decision = jeu.strategie.decider_achat(joueur, self)
                if decision:
                    joueur.acheter_propriete(self)
                    print(f"  → {joueur.nom} achète {self.nom} pour {self.prix}€")
                else:
                    print(f"  → {joueur.nom} refuse d'acheter {self.nom}")
            else:
                print(f"  → {joueur.nom} n'a pas assez d'argent pour {self.nom}")
        
        elif self.proprietaire != joueur:
            # Payer le loyer au propriétaire
            loyer = self.calculer_loyer()
            if loyer > 0:
                print(f"  → {joueur.nom} paie {loyer}€ de loyer à {self.proprietaire.nom}")
                joueur.payer(loyer, self.proprietaire)
                if hasattr(jeu, 'stats'):
                    jeu.stats.enregistrer_loyer(self, loyer)
    
    def __str__(self):
        info = f"{self.nom} ({self.couleur})"
        if self.proprietaire:
            info += f" - {self.proprietaire.nom}"
            if self.a_hotel:
                info += " []"
            elif self.nb_maisons > 0:
                info += f" [{self.nb_maisons}]"
        return info
