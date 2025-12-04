"""
TP Monopoly - Squelette de code
Durée: 16h sur 4 séances de 4h
"""

import random
from typing import List, Optional
from Carte import Carte
from Global import *

class PaquetCartes:
    cartesChance = []
    cartesCommunaute = []
    """Gère un paquet de cartes (Chance ou Communauté)"""
    def __init__(self, type_paquet: str):
        self.type_paquet = type_paquet
        self.cartes: List['Carte'] = [] 
        self.pioche: List['Carte'] = []
        self._creer_cartes()
        self._melanger()
    
    def _creer_cartes(self):
        """Crée les cartes du paquet"""
        if self.type_paquet == "chance":
            PaquetCartes.cartesChance = [
                Carte(
                    "Avancez jusqu'à la case Départ",
                    lambda j, g: self._avancer_case(j, g, 0)
                ),
                Carte(
                    "Rendez-vous Rue de la Paix.",
                    lambda j, g: self._avancer_case(j, g, 39)
                ),
                Carte(
                    "Avancez jusqu'à l'Avenue Henri-Martin. Si vous passez par la case départ, recevez 200€",
                    lambda j, g: self._avancer_case(j, g, 24)
                ),
                Carte(
                    "Avancez au Boulevard de La Villette. Si vous passez par la case départ, recevez 200€",
                    lambda j, g: self._avancer_case(j, g, 11)
                ),
                Carte(
                    "Avancez jusqu’à la Gare de Lyon. Si vous passez par la case départ, recevez 200€",
                    lambda j, g: self._avancer_case(j, g, 15)
                ),
                Carte(
                    "Rendez-vous à la gare la plus proche. Si vous passez par la case départ, recevez 200€",
                    lambda j, g: self._avancer_gare(j, g, 15)
                ),
                Carte(
                    "Reculez de 3 cases",
                    lambda j, g: self._reculer_case(j, g, 3)
                ),
                Carte(
                    "Allez en prison",
                    lambda j, g: j.aller_en_prison()
                ),
                Carte(
                    "Vous êtes libéré de prison. Cette carte peut être conservée jusqu’à ce qu’elle soit utilisée ou vendue.",
                    lambda j, g: self._donner_carte_liberte(j)
                ),
                Carte(
                    "Vous êtes imposé pour les réparations de voirie à raison de 40€ par maison et 115€ par hôtel.",
                    lambda j, g: self._payer_reparations(j, 40, 115)
                ),
                Carte(
                    "Faites des réparations dans toutes vos maisons. Versez pour chaque maison 25€, et pour chaque hôtel 100€",
                    lambda j, g: self._payer_reparations(j, 25, 100)
                ),
                Carte(
                    "Amende pour excès de vitesse : payez 15€",
                    lambda j, g: j.payer(15)
                ),
                Carte(
                    "Amende pour ivresse : payez 20€",
                    lambda j, g: j.payer(20)
                ),
                Carte(
                    "Payez pour frais de scolarité : 150€",
                    lambda j, g: j.payer(150)
                ),
                Carte(
                    "La banque vous verse un dividende de 50€",
                    lambda j, g: j.recevoir(50)
                ),
                Carte(
                    "Votre immeuble et votre prêt rapportent : touchez 150€",
                    lambda j, g: j.recevoir(150)
                ),
                Carte(
                    "Vous avez gagné le prix des mots croisés : recevez 100€",
                    lambda j, g: j.recevoir(100)
                ),
            ]
            self.cartes = PaquetCartes.cartesChance

        else:  # Caisse de Communauté
            PaquetCartes.cartesCommunaute = [
                Carte(
                    "Avancez jusqu'à la case Départ",
                    lambda j, g: self._avancer_case(j, g, 0)
                ),
                Carte(
                    "Erreur de la banque en votre faveur: recevez 200€",
                    lambda j, g: j.recevoir(200)
                ),
                Carte(
                    "Payez une amende de 10€",
                    lambda j, g: j.payer(10)
                ),
                Carte(
                    "Allez en prison",
                    lambda j, g: j.aller_en_prison()
                ),
                Carte(
                    "Vous êtes libéré de prison (gardez cette carte)",
                    lambda j, g: self._donner_carte_liberte(j)
                ),
                Carte(
                    "Les contributions vous rapportent 100€",
                    lambda j, g: j.recevoir(100)
                ),
                Carte(
                    "Recevez votre revenu annuel: 100€",
                    lambda j, g: j.recevoir(100)
                ),
                Carte(
                    "C'est votre anniversaire: recevez 10€ de chaque joueur",
                    lambda j, g: self._anniversaire(j, g)
                ),
                Carte(
                    "Amende pour ivresse: 20€",
                    lambda j, g: j.payer(20)
                ),
                Carte(
                    "Vous avez gagné le deuxième prix de beauté: 10€",
                    lambda j, g: j.recevoir(10)
                ),
            ]
            self.cartes = PaquetCartes.cartesCommunaute
          
    def _melanger(self):
        """Ouvrir un nouveau paquet"""
        self.pioche = self.cartes.copy()
        """et mélange le paquet de cartes"""
        random.shuffle(self.pioche)

    def piocher_et_executer(self, joueur: 'Joueur', jeu: 'Monopoly'):
        """Pioche une carte et exécute son action"""
        if not self.pioche:
            self._melanger()
        
        carte = self.pioche.pop()
        carte.executer(joueur, jeu)

# Fonctions utilitaires pour les actions des cartes   
    def _avancer_case(self, joueur: 'Joueur', jeu: 'Monopoly', position: int):
        """Fait avancer le joueur jusqu'à une position"""
        ancienne_pos = joueur.position
        if position < ancienne_pos:
            joueur.recevoir(ARGENT_PASSAGE_DEPART)
            print(f"      → Passage par Départ (+{ARGENT_PASSAGE_DEPART}€)")
        joueur.position = position
        case = jeu.plateau.get_case(position)
        print(f"      → {joueur.nom} avance jusqu'à {case.nom}")
        case.action(joueur, jeu)
    
    def _reculer_case(self, joueur: 'Joueur', jeu: 'Monopoly', nb_cases: int):
        """Fait reculer le joueur"""
        joueur.position = (joueur.position - nb_cases) % NOMBRE_CASES
        case = jeu.plateau.get_case(joueur.position)
        print(f"      → {joueur.nom} recule jusqu'à {case.nom}")
        case.action(joueur, jeu)
    
    def _donner_carte_liberte(self, joueur: 'Joueur'):
        """Donne une carte 'Sortie de prison' au joueur"""
        joueur.cartes_liberte += 1
        print(f"      → {joueur.nom} garde cette carte")
    
    def _payer_reparations(self, joueur: 'Joueur', prix_maison: int, prix_hotel: int):
        """Fait payer des réparations selon le nombre de maisons/hôtels"""
        total = 0
        for prop in joueur.proprietes:
            if isinstance(prop, Propriete) and not isinstance(prop, (Gare, Compagnie)):
                if prop.a_hotel:
                    total += prix_hotel
                else:
                    total += prop.nb_maisons * prix_maison
        print(f"      → {joueur.nom} paie {total}€ de réparations")
        joueur.payer(total)
    
    def _anniversaire(self, joueur: 'Joueur', jeu: 'Monopoly'):
        """Chaque autre joueur donne 10€ au joueur"""
        for autre in jeu.joueurs:
            if autre != joueur and not autre.est_en_faillite:
                autre.payer(10, joueur)
                print(f"      → {autre.nom} offre 10€ à {joueur.nom}")
    
    def _avancer_gare(self, joueur: 'Joueur', jeu: 'Monopoly'):
        """Avance jusqu'à la gare la plus proche"""
        gares = [5, 15, 25, 35]
        distances = [(g - joueur.position) % NOMBRE_CASES for g in gares]
        prochaine_gare = gares[distances.index(min(distances))]
        self._avancer_case(joueur, jeu, prochaine_gare)

# test
if __name__ == '__main__':
    paquetCartesChances = PaquetCartes("chance")

    for c in paquetCartesChances.cartes:
        print(f"{c.description}")


