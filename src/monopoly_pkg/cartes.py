from typing import List


class CarteCommunaute:
    def __init__(self, description: str, action):
        self.description = description
        self.action = action


class PaquetCartes:
    def __init__(self, type_paquet: str):
        self.type_paquet = type_paquet
        self.cartes: List[CarteCommunaute] = []
        self.pioche: List[CarteCommunaute] = []
        self._creer_cartes()
        self._melanger()

    def _avancer_case(self, joueur, jeu, position):
        joueur.position = position
        case = jeu.plateau.get_case(joueur.position)
        case.action(joueur, jeu)

    def _reculer(self, joueur, jeu, nb_cases):
        joueur.position = (joueur.position - nb_cases) % len(jeu.plateau.cases)
        case = jeu.plateau.get_case(joueur.position)
        case.action(joueur, jeu)

    def _anniversaire(self, joueur, jeu):
        for j in jeu.joueurs:
            if j is not joueur and not j.est_en_faillite:
                j.payer(10, beneficiaire=joueur)

    def _payer_reparations(self, joueur, prix_maison, prix_hotel):
        nb_maisons = 0
        nb_hotels = 0
        for p in joueur.proprietes:
            nb_maisons += p.nb_maisons
            if p.a_hotel:
                nb_hotels += 1
        total = nb_maisons * prix_maison + nb_hotels * prix_hotel
        if total > 0:
            joueur.payer(total)

    def _creer_cartes(self):
        self.cartes = []
        self.pioche = []

    def _melanger(self):
        import random as _random
        try:
            _random.shuffle(self.cartes)
        except Exception:
            pass
        self.pioche = list(self.cartes)

    def piocher(self) -> CarteCommunaute:
        if not self.pioche:
            self._melanger()
        if not self.pioche:
            return CarteCommunaute("Carte neutre (rien)", lambda j, jeu: None)
        carte = self.pioche.pop(0)
        return carte
