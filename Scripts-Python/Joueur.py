"""
TP Monopoly - Squelette de code
Durée: 16h sur 4 séances de 4h
"""
from Global import *
from typing import List, Optional

class Joueur:
    """Représente un joueur de Monopoly"""
    def __init__(self, nom: str, argent_initial: int = 1500):
        self.nom = nom
        self.argent = argent_initial
        self.position = 0
        self.proprietes: List['Propriete'] = [] # type: ignore
        self.en_prison = False
        self.tours_en_prison = 0
        self.cartes_liberte = 0
        self.est_en_faillite = False
        self.doubles_consecutifs = 0
    
    def deplacer(self, nombre_cases: int, plateau_taille: int = 40):
        """Déplace le joueur sur le plateau"""
        ancienne_position = self.position
        self.position = (self.position + nombre_cases) % plateau_taille
        
        # Vérifier le passage par la case Départ (position 0)
        if ancienne_position > self.position and ancienne_position != 0:
            self.recevoir(ARGENT_PASSAGE_DEPART)
            print(f"  → {self.nom} passe par la case Départ (+{ARGENT_PASSAGE_DEPART}€)")
            return True
        return False
    
    def aller_en_prison(self):
        """Envoie le joueur en prison"""
        self.en_prison = True
        self.tours_en_prison = 0
        self.position = 10  # Case prison
        self.doubles_consecutifs = 0
    
    def sortir_de_prison(self):
        """Libère le joueur de prison"""
        self.en_prison = False
        self.tours_en_prison = 0

    def payer(self, montant: int, beneficiaire: Optional['Joueur'] = None):
        """Le joueur paye un montant (à un autre joueur ou à la banque)"""
        if montant <= 0:
            return
        
        if self.argent >= montant:
            self.argent -= montant
            if beneficiaire:
                beneficiaire.recevoir(montant)
        else:
            # Faillite
            print(f"    {self.nom} n'a pas assez d'argent! (a {self.argent}€, doit {montant}€)")
            self.declarer_faillite(beneficiaire)
    
    def recevoir(self, montant: int):
        """Le joueur reçoit de l'argent"""
        if montant > 0:
            self.argent += montant
    
    def acheter_propriete(self, propriete: 'Propriete') -> bool:
        """Achète une propriété si le joueur a assez d'argent"""
        if propriete.proprietaire is not None:
            return False
        if self.argent < propriete.prix:
            return False
        
        self.argent -= propriete.prix
        propriete.proprietaire = self
        self.proprietes.append(propriete)
        return True
    
    def possede_quartier_complet(self, couleur: str) -> bool: # type: ignore
        """Vérifie si le joueur possède toutes les propriétés d'une couleur"""
        if couleur in ["gare", "compagnie"]:
            return False
        
        nb_par_couleur = {
        "marron": 2, "bleu_clair": 3, "rose": 3, "orange": 3,"rouge": 3,
        "jaune": 3, "vert": 3, "bleu_fonce": 2
        }

        lesProprietesDeLaCouleur = [p for p in self.proprietes
                                 if hasattr(p,'couleur') and p.couleur==couleur
                                 ]
        
        nb_requis = nb_par_couleur.get(couleur, 3)
        return len(lesProprietesDeLaCouleur) >= nb_requis


    def declarer_faillite(self, creancier: Optional['Joueur'] = None):
        """Déclare le joueur en faillite"""
        print(f"{self.nom} fait FAILLITE!")
        self.est_en_faillite = True
        
        # Transférer les propriétés au créancier ou les libérer
        for propriete in self.proprietes:
            if creancier:
                propriete.proprietaire = creancier
                creancier.proprietes.append(propriete)
                print(f"     → {propriete.nom} transférée à {creancier.nom}")
            else:
                # Libérer la propriété (remise à la banque)
                propriete.proprietaire = None
                propriete.nb_maisons = 0
                propriete.a_hotel = False
                propriete.hypothequee = False
        
        self.proprietes.clear()
        self.argent = 0
    
    def calculer_valeur_totale(self) -> int:
        """Calcule la valeur totale du joueur (argent + propriétés)"""
        valeur = self.argent
        for prop in self.proprietes:
            valeur += prop.prix
            if isinstance(prop, Propriete) and not isinstance(prop, (Gare, Compagnie)):
                valeur += prop.nb_maisons * prop.prix_maison
                if prop.a_hotel:
                    valeur += prop.prix_maison
        return valeur
    
    def __str__(self):
        status = f"{self.nom}: {self.argent}€"
        if self.en_prison:
            status += " [PRISON]"
        if self.est_en_faillite:
            status += " [FAILLITE]"
        return status

   