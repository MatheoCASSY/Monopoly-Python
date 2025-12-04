"""
TP Monopoly - Squelette de code
Durée: 16h sur 4 séances de 4h
"""
from Case import Case

from typing import Optional
from Quartier import Quartier

class Propriete(Case):
    """Case représentant une propriété achetable"""
    def __init__(self, nom: str, position: int, prix: int, loyer: int, couleur: str, prix_maison: int = 50):
        super().__init__(nom, position)
        self.prix = prix
        self.loyer_base = loyer
        self.couleur = couleur
        self.proprietaire: Optional['Joueur'] = None # type: ignore
        # nb_maisons: 0-4 = maisons, 5 = hôtel
        self.nb_maisons = 0
        # Référence au quartier (sera assignée par Plateau)
        self.quartier: Optional[Quartier] = None
        self.prix_maison = prix_maison
        self.hypothequee = False
    
    def calculer_loyer(self) -> int:
        """Calcule le loyer en fonction des maisons/hôtels"""
        if self.hypothequee or not self.proprietaire:
            return 0
        
        # Hôtel = 5e maison
        if self.nb_maisons == 5:
            return self.loyer_base * 100
        elif 1 <= self.nb_maisons <= 4:
            # Multiplicateurs: 1 maison=×5, 2=×15, 3=×45, 4=×80
            multiplicateurs = [5, 15, 45, 80]
            return self.loyer_base * multiplicateurs[self.nb_maisons - 1]
        else:
            # Si le quartier est connu, interroger l'objet Quartier
            if self.quartier is not None:
                if self.quartier.possederQuartier(self.proprietaire):
                    return self.loyer_base * 2
            elif self.proprietaire and self.proprietaire.possede_quartier_complet(self.couleur):
                # fallback sur l'ancien mécanisme
                return self.loyer_base * 2
        return self.loyer_base
    

    def peut_construire(self, joueur: 'Joueur', ignorer_repartition: bool = False) -> bool:
        """Vérifie si on peut construire sur cette propriété"""
        if self.proprietaire != joueur:
            return False
        
        if joueur.est_en_faillite:
            return False
        
        if joueur.argent < self.prix_maison:
            return False
        
        # Vérifier via l'objet Quartier si disponible
        if self.quartier is not None:
            if not self.quartier.possederQuartier(joueur):
                return False
        else:
            if not joueur.possede_quartier_complet(self.couleur):
                return False
          
        if self.hypothequee:
            return False
        
        # si déjà hôtel (5 maisons) -> pas possible
        if self.nb_maisons == 5:
            return False

        # Respecter la répartition équilibrée sauf si on force la construction
        if not ignorer_repartition:
            nbMaisonsMin = min([p.nb_maisons for p in joueur.proprietes])
            if self.nb_maisons > nbMaisonsMin:
                return False
        
        # ici ok
        return True
    
    def construire_maison(self, joueur: 'Joueur', forcer: bool = False) -> bool:
        """Construit une maison (maximum 4)"""
        if not self.peut_construire(joueur, ignorer_repartition=forcer):
            return False
        
        # Autorisé jusqu'à 5 (5 représente l'hôtel)
        if self.nb_maisons >= 5:
            return False
        
        if joueur.argent < self.prix_maison:
            return False
        
        joueur.payer(self.prix_maison)
        self.nb_maisons += 1
        # Enregistrer la construction sur le joueur
        try:
            joueur.maisons_construites += 1
        except Exception:
            pass
        return True
    
    def construire_hotel(self, joueur: 'Joueur', forcer: bool = False) -> bool:
        """Construit un hôtel (nécessite 4 maisons)"""
        # Allow forcing via peut_construire's ignorer_repartition if needed
        if not self.peut_construire(joueur, ignorer_repartition=forcer):
            return False
        if self.nb_maisons != 4:
            return False

        if joueur.argent < self.prix_maison * 5:
            return False

        # Construire l'hôtel comme la 5ème maison — coût = 5 × prix_maison
        joueur.payer(self.prix_maison * 5)
        self.nb_maisons = 5
        # Enregistrer l'hôtel construit sur le joueur
        try:
            joueur.hotels_construits += 1
        except Exception:
            pass
        return True
   
    def action(self, joueur: 'Joueur', jeu: 'Monopoly'):
        """Gère l'arrivée d'un joueur sur la propriété"""
        if self.proprietaire is None:
            # Propriété libre - proposer l'achat
            if joueur.argent >= self.prix:
                # Use the player's strategy if available, otherwise default to buying
                strat = getattr(joueur, 'strategie', None)
                if strat is not None and hasattr(strat, 'decider_achat'):
                    decision = strat.decider_achat(joueur, self)
                else:
                    decision = True

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
            if self.nb_maisons == 5:
                info += " [HÔTEL]"
            elif self.nb_maisons > 0:
                info += f" [{self.nb_maisons}]"
        return info
