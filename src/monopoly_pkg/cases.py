from typing import Optional


class Case:
    """Classe de base pour toutes les cases du plateau"""
    def __init__(self, nom: str, position: int):
        self.nom = nom
        self.position = position

    def action(self, joueur: 'Joueur', jeu: 'Monopoly'):
        pass


class Propriete(Case):
    def __init__(self, nom: str, position: int, prix: int, loyer: int, couleur: str):
        super().__init__(nom, position)
        self.prix = prix
        self.loyer_base = loyer
        self.couleur = couleur
        self.proprietaire: Optional['Joueur'] = None
        self.nb_maisons = 0
        self.a_hotel = False

    def calculer_loyer(self) -> int:
        if self.loyer_base == 0:
            return 0
        if self.nb_maisons == 0 and not self.a_hotel:
            proprio = self.proprietaire
            if proprio and proprio.possede_quartier_complet(self.couleur):
                return self.loyer_base * 2
            return self.loyer_base
        if self.a_hotel:
            return self.loyer_base * 32
        progressions = [0.3, 0.9, 1.6, 2.5]
        return int(self.loyer_base * (1 + progressions[self.nb_maisons - 1]))

    def action(self, joueur: 'Joueur', jeu: 'Monopoly'):
        if self.proprietaire is None:
            if joueur.argent >= self.prix:
                reponse = input(f"{joueur.nom}, veux-tu acheter {self.nom} pour {self.prix}€ ? (Oui/Non) ").strip().lower()
                if reponse.startswith("oui"):
                    succes = joueur.acheter_propriete(self)
                    if succes:
                        print(f"{joueur.nom} achète {self.nom}.")
                    else:
                        print(f"Achat de {self.nom} impossible.")
                else:
                    print(f"{joueur.nom} refuse d'acheter {self.nom}.")
            else:
                print(f"{joueur.nom} n'a pas assez d'argent pour acheter {self.nom}.")
            return
        if self.proprietaire == joueur:
            print(f"{joueur.nom} est chez lui sur {self.nom}, il ne paie rien.")
            return
        proprio = self.proprietaire
        loyer = self.calculer_loyer()
        print(f"{joueur.nom} est tombé sur {self.nom} appartenant à {proprio.nom} et doit payer {loyer}€ de loyer.")
        succes = joueur.payer(loyer, beneficiaire=proprio)
        try:
            if hasattr(jeu, 'stats'):
                jeu.stats.enregistrer_loyer(self, loyer)
        except Exception:
            pass


class Gare(Propriete):
    def __init__(self, nom, position):
        super().__init__(nom, position, prix=200, loyer=25, couleur='gare')

    def calculer_loyer(self) -> int:
        if not self.proprietaire:
            return 0
        nb_gares = sum(1 for p in self.proprietaire.proprietes if isinstance(p, Gare))
        tarifs = {1: 25, 2: 50, 3: 100, 4: 200}
        return tarifs.get(nb_gares, 0)


class Compagnie(Propriete):
    def __init__(self, nom, position, prix: int = 150):
        super().__init__(nom, position, prix=prix, loyer=0, couleur='compagnie')
        self.dernier_lancer_des = 0

    def calculer_loyer(self) -> int:
        if not self.proprietaire:
            return 0
        nb_compagnies = sum(1 for p in self.proprietaire.proprietes if isinstance(p, Compagnie))
        multiplicateur = {1: 4, 2: 10}.get(nb_compagnies, 0)
        return multiplicateur * self.dernier_lancer_des

    def action(self, joueur: 'Joueur', jeu: 'Monopoly'):
        self.dernier_lancer_des = jeu.dernier_total_des
        super().action(joueur, jeu)


from enum import Enum


class TypeCase(Enum):
    DEPART = "depart"
    PRISON = "prison"
    TAXE = "taxe"
    CHANCE = "chance"
    CAISSE_DE_COMMUNAUTE = "caisse"
    ALLEZ_PRISON = "allez_prison"
    PARC_GRATUIT = "parc_gratuit"
    IMPOT = "impot"


class CaseSpeciale(Case):
    def __init__(self, nom: str, position: int, type_case: TypeCase):
        super().__init__(nom, position)
        self.type_case = type_case

    def action(self, joueur: 'Joueur', jeu: 'Monopoly'):
        if self.type_case == TypeCase.DEPART:
            joueur.recevoir(200)
        elif self.type_case == TypeCase.PRISON:
            if joueur.en_prison:
                print(f"{joueur.nom} est en prison (tour {joueur.tours_en_prison}).")
            else:
                print(f"{joueur.nom} est simplement en visite à la prison.")
        elif self.type_case == TypeCase.ALLEZ_PRISON:
            joueur.aller_en_prison()
        elif self.type_case in (TypeCase.TAXE, TypeCase.IMPOT):
            if self.nom == "Impot sur le revenu":
                montant = 200
            elif self.nom == "Taxe de Luxe":
                montant = 100
            else:
                montant = 100
            joueur.payer(montant)
        elif self.type_case == TypeCase.CHANCE:
            carte = jeu.cartes_chance.piocher()
            print(carte.description)
            carte.action(joueur, jeu)
        elif self.type_case == TypeCase.CAISSE_DE_COMMUNAUTE:
            carte = jeu.cartes_communaute.piocher()
            print(carte.description)
            carte.action(joueur, jeu)
        elif self.type_case == TypeCase.PARC_GRATUIT:
            pass
