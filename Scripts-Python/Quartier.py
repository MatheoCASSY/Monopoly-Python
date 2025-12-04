from typing import List, Optional

class Quartier:
    """Représente un quartier (couleur) du plateau.

    Attributs:
    - couleur: identifiant du quartier (string)
    - prix_maison: coût d'une maison dans ce quartier
    - proprietes: liste des objets Propriete appartenant au quartier
    """
    def __init__(self, couleur: str, prix_maison: int):
        self.couleur = couleur
        self.prix_maison = prix_maison
        self.proprietes: List['Propriete'] = []  # type: ignore

    def ajouter_propriete(self, prop: 'Propriete'):
        self.proprietes.append(prop)

    def possederQuartier(self, joueur: 'Joueur') -> bool:
        """Retourne True si le joueur possède toutes les propriétés du quartier."""
        if joueur is None:
            return False
        # Toutes les propriétés du quartier doivent avoir pour proprietaire le joueur
        for p in self.proprietes:
            if p.proprietaire != joueur:
                return False
        return True

    def __str__(self):
        return f"Quartier({self.couleur}, maisons={self.prix_maison}, nb_props={len(self.proprietes)})"
