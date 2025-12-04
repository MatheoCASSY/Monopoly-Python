from typing import List, Optional


class Joueur:
    def __init__(self, nom: str, argent_initial: int = 1500):
        self.nom = nom
        self.argent = argent_initial
        self.position = 0
        self.proprietes: List['Propriete'] = []
        self.en_prison = False
        self.tours_en_prison = 0
        self.est_en_faillite = False
        self.doubles_consecutifs = 0
        self.cartes_liberte = 0

    def sortir_de_prison(self):
        self.en_prison = False
        self.tours_en_prison = 0

    def deplacer(self, nombre_cases: int, plateau_taille: int = 40) -> bool:
        ancienne_position = self.position
        nouvelle_position = (ancienne_position + nombre_cases) % plateau_taille
        est_passe_par_depart = (ancienne_position + nombre_cases) >= plateau_taille
        self.position = nouvelle_position
        if est_passe_par_depart:
            self.argent += 200
        return est_passe_par_depart

    def payer(self, montant: int, beneficiaire: Optional['Joueur'] = None) -> bool:
        if self.est_en_faillite:
            return False
        if self.argent >= montant:
            self.argent -= montant
            if beneficiaire is not None:
                beneficiaire.argent += montant
            return True
        montant_effectif = self.argent
        if beneficiaire is not None and montant_effectif > 0:
            beneficiaire.argent += montant_effectif
        self.argent = 0
        self.est_en_faillite = True
        if beneficiaire is not None and self.proprietes:
            for prop in self.proprietes:
                prop.proprietaire = beneficiaire
                beneficiaire.proprietes.append(prop)
            self.proprietes.clear()
        else:
            for prop in self.proprietes:
                prop.proprietaire = None
            self.proprietes.clear()
        return False

    def recevoir(self, montant: int):
        self.argent += montant

    def acheter_propriete(self, propriete: 'Propriete') -> bool:
        if propriete.proprietaire is not None:
            return False
        if self.argent < propriete.prix:
            return False
        self.argent -= propriete.prix
        propriete.proprietaire = self
        self.proprietes.append(propriete)
        return True

    def possede_quartier_complet(self, couleur: str) -> bool:
        if couleur in ('gare', 'compagnie'):
            return False
        nb_par_couleur = {
            "marron": 2, "bleu_clair": 3, "rose": 3, "orange": 3,
            "rouge": 3, "jaune": 3, "vert": 3, "bleu_fonce": 2
        }
        if couleur not in nb_par_couleur:
            return False
        proprietes_couleur = [p for p in self.proprietes if hasattr(p, 'couleur') and p.couleur == couleur]
        return len(proprietes_couleur) == nb_par_couleur[couleur]

    def peut_construire_maison(self, propriete: 'Propriete') -> bool:
        if propriete.proprietaire != self:
            return False
        if propriete.nb_maisons >= 4:
            return False
        if propriete.a_hotel:
            return False
        if not self.possede_quartier_complet(propriete.couleur):
            return False
        return True

    def construire_maison(self, propriete: 'Propriete') -> bool:
        if not self.peut_construire_maison(propriete):
            return False
        prix_maison = propriete.prix // 2
        if self.argent < prix_maison:
            return False
        self.argent -= prix_maison
        propriete.nb_maisons += 1
        return True

    def construire_hotel(self, propriete: 'Propriete') -> bool:
        if propriete.proprietaire != self:
            return False
        if propriete.nb_maisons != 4:
            return False
        if propriete.a_hotel:
            return False
        prix_hotel = (propriete.prix // 2) * 5
        if self.argent < prix_hotel:
            return False
        self.argent -= prix_hotel
        propriete.a_hotel = True
        propriete.nb_maisons = 0
        return True

    def possede_quartier(self, couleur: str, toutes_proprietes: List['Propriete']) -> bool:
        return self.possede_quartier_complet(couleur)

    def aller_en_prison(self):
        self.position = 10
        self.en_prison = True
        self.tours_en_prison = 0
        self.doubles_consecutifs = 0
