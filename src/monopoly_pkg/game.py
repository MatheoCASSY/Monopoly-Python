import random
from typing import List, Optional

from .plateau import Plateau
from .joueur import Joueur
from .cartes import PaquetCartes
from .stats import StatistiquesPartie


class Monopoly:
    def __init__(self, noms_joueurs: List[str]):
        self.plateau = Plateau()
        self.joueurs = [Joueur(nom) for nom in noms_joueurs]
        self.joueur_actuel_index = 0
        self.cartes_chance = PaquetCartes("chance")
        self.cartes_communaute = PaquetCartes("communaute")
        self.tour_numero = 0
        self.dernier_total_des = 0
        self.stats = StatistiquesPartie()

    def gerer_prison(self, joueur: Joueur) -> bool:
        if joueur.cartes_liberte > 0:
            rep = input("Utiliser une carte 'Libéré de prison' ? (o/n): ").strip().lower()
            if rep == "o":
                joueur.cartes_liberte -= 1
                joueur.sortir_de_prison()
                return False
        if joueur.argent >= 50:
            rep = input("Payer 50€ pour sortir immédiatement ? (o/n): ").strip().lower()
            if rep == "o":
                joueur.payer(50)
                joueur.sortir_de_prison()
                return False
        de1, de2 = self.lancer_des()
        if de1 == de2:
            joueur.sortir_de_prison()
            joueur.deplacer(de1 + de2)
            case = self.plateau.get_case(joueur.position)
            case.action(joueur, self)
            return True
        else:
            joueur.tours_en_prison += 1
            if joueur.tours_en_prison >= 3:
                joueur.payer(50)
                joueur.sortir_de_prison()
                joueur.deplacer(de1 + de2)
                case = self.plateau.get_case(joueur.position)
                case.action(joueur, self)
                return True
            else:
                return True

    def lancer_des(self) -> tuple:
        return random.randint(1, 6), random.randint(1, 6)

    def jouer_tour(self, joueur: Joueur):
        if joueur.est_en_faillite:
            return
        if joueur.en_prison:
            tour_consomme = self.gerer_prison(joueur)
            if tour_consomme:
                return
        de1, de2 = self.lancer_des()
        total = de1 + de2
        self.dernier_total_des = total
        a_passe_depart = joueur.deplacer(total)
        case = self.plateau.get_case(joueur.position)
        try:
            self.stats.enregistrer_passage(case)
        except Exception:
            pass
        case.action(joueur, self)
        if de1 == de2:
            joueur.doubles_consecutifs += 1
            if joueur.doubles_consecutifs >= 3:
                joueur.aller_en_prison()
            else:
                self.jouer_tour(joueur)
        else:
            joueur.doubles_consecutifs = 0

    def partie_terminee(self) -> bool:
        joueurs_actifs = [j for j in self.joueurs if not j.est_en_faillite]
        return len(joueurs_actifs) <= 1

    def obtenir_gagnant(self) -> Optional[Joueur]:
        joueurs_actifs = [j for j in self.joueurs if not j.est_en_faillite]
        return joueurs_actifs[0] if len(joueurs_actifs) == 1 else None

    def jouer_partie(self, max_tours: int = 200):
        print("=== DÉBUT DE LA PARTIE ===\n")
        while not self.partie_terminee() and self.tour_numero < max_tours:
            joueur = self.joueurs[self.joueur_actuel_index]
            if not joueur.est_en_faillite:
                self.jouer_tour(joueur)
            self.joueur_actuel_index = (self.joueur_actuel_index + 1) % len(self.joueurs)
            if self.joueur_actuel_index == 0:
                self.tour_numero += 1
        gagnant = self.obtenir_gagnant()
        if gagnant:
            print(f"\n🎉 {gagnant.nom} a gagné avec {gagnant.argent}€ !")
        else:
            print(f"\nPartie terminée après {max_tours} tours (limite atteinte)")
        return gagnant
