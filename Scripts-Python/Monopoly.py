"""
TP Monopoly - Squelette de code
Durée: 16h sur 4 séances de 4h
"""

from Global import *
from Statistiques import StatistiquesPartie
from IAAgressive import IAAgressive
from IAStrategique import IAStrategique
from StrategieIA import StrategieIA

from Plateau import Plateau
from Joueur import Joueur
from Propriete import Propriete
from Gare import Gare
from Compagnie import Compagnie
from PaquetCartes import PaquetCartes

import random
from typing import List, Optional

class Monopoly:
    """Classe principale qui gère une partie de Monopoly"""
    def __init__(self, noms_joueurs: List[str], strategie: 'StrategieIA' | List['StrategieIA'] = None):
        self.plateau = Plateau()
        self.joueurs = [Joueur(nom) for nom in noms_joueurs]
        self.joueur_actuel_index = 0
        self.cartes_chance = PaquetCartes("chance")
        self.cartes_communaute = PaquetCartes("communaute")
        self.tour_numero = 0
        self.dernier_total_des = 0
        # Support either a single strategy (applied to all players) or a list of strategies per player
        if isinstance(strategie, list):
            # normalize length: repeat last if shorter
            if len(strategie) < len(self.joueurs):
                strategie = strategie + [strategie[-1]] * (len(self.joueurs) - len(strategie))
            self.strategies = strategie[:len(self.joueurs)]
        else:
            base = strategie or IAAgressive()
            self.strategies = [base for _ in self.joueurs]

        # Attach strategy to each Joueur for per-player decisions
        for idx, j in enumerate(self.joueurs):
            try:
                j.strategie = self.strategies[idx]
            except Exception:
                j.strategie = self.strategies[0]
        self.stats = StatistiquesPartie()
        self.mode_debug = False
    
    def lancer_des(self) -> tuple[int, int]:
        """Lance deux dés et retourne les valeurs"""
        de1 = random.randint(1, 6)
        de2 = random.randint(1, 6)
        return de1, de2
    
    def jouer_tour(self, joueur: Joueur):
        """Joue un tour complet pour un joueur"""
        if joueur.est_en_faillite:
            return
        
        if not self.mode_debug:
            print(f"\n{'='*60}")
            print(f"Tour de {joueur.nom}")
            print(f"{'='*60}")
            print(f"Argent: {joueur.argent}€ | 📍 Position: {self.plateau.get_case(joueur.position).nom}")
            
            if len(joueur.proprietes) > 0:
                print(f"Propriétés: {len(joueur.proprietes)}")
        
        # Gestion de la prison
        if joueur.en_prison:
            self._gerer_prison(joueur)
            if joueur.en_prison:  # Toujours en prison après gestion
                return
        
        # Lancer les dés
        de1, de2 = self.lancer_des()
        total = de1 + de2
        self.dernier_total_des = total
        est_double = (de1 == de2)
        
        if not self.mode_debug:
            print(f"Dés: {de1} + {de2} = {total}" + (" (DOUBLE!)" if est_double else ""))
        
        # Vérifier les doubles consécutifs
        if est_double:
            joueur.doubles_consecutifs += 1
            if joueur.doubles_consecutifs >= 3:
                if not self.mode_debug:
                    print("3 doubles consécutifs! Direction la prison!")
                joueur.aller_en_prison()
                return
        else:
            joueur.doubles_consecutifs = 0
        
        # Déplacer le joueur
        joueur.deplacer(total)
        case_arrivee = self.plateau.get_case(joueur.position)
        
        if not self.mode_debug:
            print(f"Arrivée sur: {case_arrivee}")
        
        # Enregistrer le passage pour les statistiques
        self.stats.enregistrer_passage(case_arrivee)
        
        # Exécuter l'action de la case
        case_arrivee.action(joueur, self)
        
        # Proposer des constructions si quartier
        if not joueur.est_en_faillite:
            self._proposer_constructions(joueur)
        
        # Rejouer si double (et pas en prison)
        if est_double and not joueur.en_prison and not joueur.est_en_faillite:
            if not self.mode_debug:
                print("Double! Vous rejouez!")
            self.jouer_tour(joueur)
    
    def _gerer_prison(self, joueur: Joueur):
        """Gère les différentes options pour sortir de prison"""
        joueur.tours_en_prison += 1
        
        if not self.mode_debug:
            print(f"{joueur.nom} est en prison (tour {joueur.tours_en_prison}/3)")
        
        # Option 1: Utiliser une carte libération
        if joueur.cartes_liberte > 0:
            if not self.mode_debug:
                print("  → Utilisation d'une carte 'Sortie de prison'")
            joueur.cartes_liberte -= 1
            joueur.sortir_de_prison()
            return
        
        # Option 2: Payer 50€
        if joueur.argent >= PRIX_SORTIE_PRISON:
            if not self.mode_debug:
                print(f"  → Paiement de {PRIX_SORTIE_PRISON}€ pour sortir")
            joueur.payer(PRIX_SORTIE_PRISON)
            joueur.sortir_de_prison()
            return
        
        # Option 3: Tenter un double
        de1, de2 = self.lancer_des()
        if not self.mode_debug:
            print(f"Tentative de double: {de1} et {de2}")
        
        if de1 == de2:
            if not self.mode_debug:
                print("Double! Sortie de prison!")
            joueur.sortir_de_prison()
            joueur.deplacer(de1 + de2)
            case = self.plateau.get_case(joueur.position)
            if not self.mode_debug:
                print(f"Arrivée sur: {case}")
            case.action(joueur, self)
        elif joueur.tours_en_prison >= 3:
            if not self.mode_debug:
                print(f"3 tours écoulés! Sortie forcée ({PRIX_SORTIE_PRISON}€)")
            joueur.payer(PRIX_SORTIE_PRISON)
            joueur.sortir_de_prison()
            joueur.deplacer(de1 + de2)
            case = self.plateau.get_case(joueur.position)
            if not self.mode_debug:
                print(f"Arrivée sur: {case}")
            case.action(joueur, self)
        else:
            if not self.mode_debug:
                print("Pas de double. Reste en prison.")
    
    def _proposer_constructions(self, joueur: Joueur):
        """Propose au joueur de construire sur ses quartiers"""
        # Trouver les quartiers (regroupement par objet Quartier si présent)
        quartiers = {}
        for prop in joueur.proprietes:
            if isinstance(prop, Propriete) and not isinstance(prop, (Gare, Compagnie)):
                # Si la propriété a un objet Quartier, utiliser sa couleur comme clé
                couleur = prop.quartier.couleur if getattr(prop, 'quartier', None) is not None else prop.couleur
                # Vérifier que le joueur possède tout le quartier
                possede = False
                if getattr(prop, 'quartier', None) is not None:
                    possede = prop.quartier.possederQuartier(joueur)
                else:
                    possede = joueur.possede_quartier_complet(couleur)

                if possede:
                    if couleur not in quartiers:
                        quartiers[couleur] = []
                    quartiers[couleur].append(prop)
        
        if not quartiers:
            return
        # If an IA strategy is set and provides a construction choice, ask it repeatedly
        # Use the player's own strategy (if present) to decide constructions
        if getattr(joueur, 'strategie', None) is not None and hasattr(joueur.strategie, 'decider_construction'):
            # The strategy returns a Propriete to build on (or None). Loop while the IA requests constructions
            while True:
                try:
                    cible = joueur.strategie.decider_construction(joueur)
                except Exception:
                    # If the strategy isn't ready to decide, fallback to default behavior
                    cible = None

                # If strategy returned a property, try to build on it
                if isinstance(cible, Propriete):
                    prop = cible
                    # Ensure still constructible; affordability is checked by construire_* methods
                    if not prop.peut_construire(joueur):
                        break

                    # Allow IAStrategique to force construction (bypass repartition rules)
                    force = isinstance(joueur.strategie, IAStrategique)

                    if prop.nb_maisons < 4:
                        if prop.construire_maison(joueur, forcer=force):
                            if not self.mode_debug:
                                print(f"Construction d'une maison sur {prop.nom}")
                            # Enregistrer la construction
                            if hasattr(self, 'stats') and self.stats is not None:
                                try:
                                    self.stats.constructions.append({
                                        'tour': self.tour_numero,
                                        'joueur': joueur.nom,
                                        'propriete': prop.nom,
                                        'type': 'maison',
                                        'cout': prop.prix_maison
                                    })
                                except Exception:
                                    pass
                            # continue loop to ask strategy for next build
                            continue
                        else:
                            break
                    elif prop.nb_maisons == 4:
                        if prop.construire_hotel(joueur, forcer=force):
                            if not self.mode_debug:
                                print(f"Construction d'un hôtel sur {prop.nom}")
                            # Enregistrer la construction
                            if hasattr(self, 'stats') and self.stats is not None:
                                try:
                                    self.stats.constructions.append({
                                        'tour': self.tour_numero,
                                        'joueur': joueur.nom,
                                        'propriete': prop.nom,
                                        'type': 'hotel',
                                        'cout': prop.prix_maison * 5
                                    })
                                except Exception:
                                    pass
                            continue
                        else:
                            break
                    else:
                        break

                # If strategy returned True (legacy) or None, fall back to default simple behavior
                break

        # Fallback/simple automatic construction (kept for non-IA or legacy strategies)
        for couleur, proprietes in quartiers.items():
            for prop in proprietes:
                if prop.peut_construire(joueur):
                    # Construire si assez d'argent (garder une réserve)
                    # Hôtel est maintenant représenté par nb_maisons == 5
                    if prop.nb_maisons != 5 and joueur.argent >= prop.prix_maison * 2:
                        if prop.nb_maisons < 4:
                            if prop.construire_maison(joueur):
                                if not self.mode_debug:
                                    print(f"Construction d'une maison sur {prop.nom}")
                        elif prop.nb_maisons == 4:
                            if prop.construire_hotel(joueur):
                                if not self.mode_debug:
                                    print(f"Construction d'un hôtel sur {prop.nom}")
    
    def partie_terminee(self) -> bool:
        """Vérifie si la partie est terminée (un seul joueur restant)"""
        joueurs_actifs = [j for j in self.joueurs if not j.est_en_faillite]
        return len(joueurs_actifs) <= 1
    
    def obtenir_gagnant(self) -> Optional[Joueur]:
        """Retourne le joueur gagnant"""
        joueurs_actifs = [j for j in self.joueurs if not j.est_en_faillite]
        return joueurs_actifs[0] if len(joueurs_actifs) == 1 else None
    
    def jouer_partie(self, max_tours: int = 200, mode_interactif: bool = False) -> Optional[Joueur]:
        """
        Joue une partie complète de Monopoly.
        Retourne le gagnant ou None si limite de tours atteinte.
        """
        if not self.mode_debug:
            print("\n" + "="*60)
            print("DÉBUT DE LA PARTIE DE MONOPOLY")
            print("="*60)
            print(f"Joueurs: {', '.join(j.nom for j in self.joueurs)}")
            # Print per-player strategy summary
            try:
                summary = ", ".join(f"{j.nom} -> {getattr(j,'strategie').nom}" for j in self.joueurs)
                print(f"Stratégies IA par joueur: {summary}")
            except Exception:
                pass
            print("="*60)
        
        while not self.partie_terminee() and self.tour_numero < max_tours:
            joueur = self.joueurs[self.joueur_actuel_index]
            
            if not joueur.est_en_faillite:
                self.jouer_tour(joueur)
                
                if mode_interactif and not joueur.est_en_faillite:
                    input("\n[Appuyez sur Entrée pour le prochain joueur...]")
            
            # Passer au joueur suivant
            self.joueur_actuel_index = (self.joueur_actuel_index + 1) % len(self.joueurs)
            
            # Nouveau tour complet
            if self.joueur_actuel_index == 0:
                self.tour_numero += 1
                
                # Afficher un résumé tous les 10 tours (mode debug uniquement)
                if not self.mode_debug and self.tour_numero % 10 == 0:
                    print(f"\nTour {self.tour_numero} - État des joueurs:")
                    for j in self.joueurs:
                        if not j.est_en_faillite:
                            print(f"  {j}")
        
        # Afficher le résultat final
        self._afficher_resultat_final()
        
        self.stats.nb_tours = self.tour_numero
        gagnant = self.obtenir_gagnant()
        self.stats.gagnant = gagnant
        
        return gagnant
    
    def _afficher_resultat_final(self):
        """Affiche le résultat final de la partie"""
        if self.mode_debug:
            return
        
        print("\n" + "="*60)
        print("FIN DE LA PARTIE")
        print("="*60)
        
        gagnant = self.obtenir_gagnant()
        if gagnant:
            print(f"VICTOIRE DE {gagnant.nom}!")
            print(f"Fortune finale: {gagnant.argent}€")
            print(f"Propriétés possédées: {len(gagnant.proprietes)}")
            
            # Détail des propriétés
            if gagnant.proprietes:
                print("\nPropriétés possédées:")
                for prop in gagnant.proprietes:
                    info = f"   • {prop.nom}"
                    if isinstance(prop, Propriete) and not isinstance(prop, (Gare, Compagnie)):
                        if prop.nb_maisons == 5:
                            info += " [HÔTEL]"
                        elif prop.nb_maisons > 0:
                            info += f" [{prop.nb_maisons}]"
                    print(info)
            # Constructions réalisées
            maisons = getattr(gagnant, 'maisons_construites', 0)
            hotels = getattr(gagnant, 'hotels_construits', 0)
            print(f"\nConstructions réalisées par {gagnant.nom}: {maisons} maisons, {hotels} hôtels")
        else:
            print(f"Limite de {self.tour_numero} tours atteinte")
            
            # Classement par argent
            joueurs_vivants = [j for j in self.joueurs if not j.est_en_faillite]
            if joueurs_vivants:
                joueurs_vivants.sort(key=lambda j: j.calculer_valeur_totale(), reverse=True)
                print("\nClassement final (par valeur totale):")
                for i, j in enumerate(joueurs_vivants, 1):
                    valeur = j.calculer_valeur_totale()
                    print(f"   {i}. {j.nom}: {j.argent}€ (valeur totale: {valeur}€)")
                    maisons = getattr(j, 'maisons_construites', 0)
                    hotels = getattr(j, 'hotels_construits', 0)
                    print(f"       → Constructions: {maisons} maisons, {hotels} hôtels")



if __name__ == "__main__":
    # Test basique
    
    print("ok")

    jeu = Monopoly(["Michel"])
    
    joueur = jeu.joueurs[0]

    # Test Départ
    joueur.position = 0
    argent_avant = joueur.argent
    jeu.plateau.cases[0].action(joueur, jeu)
    assert joueur.argent == argent_avant + 200

    # Test Prison
    joueur.position = 30
    jeu.plateau.cases[30].action(joueur, jeu)
    assert joueur.en_prison == True
    assert joueur.position == 10

    # Test Impot
    joueur.position = 4
    argent_avant = joueur.argent
    jeu.plateau.cases[4].action(joueur, jeu)
    assert joueur.argent == argent_avant - 200

    # Test Parc gratuit
    joueur.position = 20
    jeu.plateau.cases[20].action(joueur, jeu)

    print(" Cases spéciales validées!")