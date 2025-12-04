"""
TP Monopoly - Squelette de code
Durée: 16h sur 4 séances de 4h
"""
from typing import List, Optional

from Monopoly import Monopoly
from Plateau import Plateau
from Joueur import Joueur
from CaseSpeciale import CaseSpeciale
from Propriete import Propriete
from Gare import Gare

from StrategieIA import StrategieIA
from IAAgressive import IAAgressive
from IAStrategique import IAStrategique
from IAConservative import IAConservative
from Statistiques import StatistiquesPartie
import random


def _read_int(prompt: str, min_val: int | None = None, max_val: int | None = None) -> int:
    """Lit un entier depuis l'entrée utilisateur de manière robuste.
    Accepte des entrées comme '4.' ou '4.0' et refuse les flottants non entiers.
    Répète la demande tant que l'entrée n'est pas valide.
    """
    while True:
        s = input(prompt).strip()
        if s == '':
            print("Entrée vide — veuillez saisir un nombre.")
            continue
        # Accept simple trailing dot (e.g. '4.') by stripping it
        if s.endswith('.'):
            s2 = s[:-1]
        else:
            s2 = s

        try:
            val = int(s2)
        except ValueError:
            # try float then check it's an integer value
            try:
                f = float(s2)
                if abs(f - round(f)) < 1e-9:
                    val = int(round(f))
                else:
                    print(f"'{s}' n'est pas un entier valide.")
                    continue
            except ValueError:
                print(f"'{s}' n'est pas un entier valide.")
                continue

        if min_val is not None and val < min_val:
            print(f"Le nombre doit être au moins {min_val}.")
            continue
        if max_val is not None and val > max_val:
            print(f"Le nombre doit être au plus {max_val}.")
            continue
        return val

def simuler_parties(nb_parties: int, nb_joueurs: int, strategie: StrategieIA = None):
    """Simule plusieurs parties et collecte des statistiques agrégées"""
    print(f"\n{'='*60}")
    print(f"SIMULATION DE {nb_parties} PARTIES")
    print(f"{'='*60}")
    
    # Determine strategies for players once at creation time.
    # If `strategie` is None -> randomize strategies per player (once) from the pool.
    # If `strategie` is a single StrategieIA -> use it for all players.
    # If `strategie` is a list -> normalize length and use per-player strategies.
    pool = [IAAgressive, IAConservative, IAStrategique]
    if strategie is None:
        strategies_for_players = [random.choice(pool)() for _ in range(nb_joueurs)]
    elif isinstance(strategie, list):
        # normalize list length
        if len(strategie) < nb_joueurs:
            strategie = strategie + [strategie[-1]] * (nb_joueurs - len(strategie))
        strategies_for_players = strategie[:nb_joueurs]
    else:
        strategies_for_players = [strategie for _ in range(nb_joueurs)]

    resultats = {f"Joueur {i+1}": 0 for i in range(nb_joueurs)}
    durees = []
    toutes_stats = []
    
    for i in range(nb_parties):
        if (i + 1) % 10 == 0 or i == 0:
            print(f"Progression: {i+1}/{nb_parties}", end='\r')
        # Use the same strategies_for_players for every simulated game
        noms = [f"Joueur {j+1} ({strategies_for_players[j].nom})" for j in range(nb_joueurs)]
        jeu = Monopoly(noms, strategies_for_players)
        jeu.mode_debug = True
        
        gagnant = jeu.jouer_partie(max_tours=200)
        # increment results by player index so aggregation is stable
        if gagnant:
            for idx, joueur in enumerate(jeu.joueurs):
                if joueur is gagnant or joueur.nom == gagnant.nom:
                    resultats[f"Joueur {idx+1}"] += 1
                    break
        durees.append(jeu.stats.nb_tours)
        toutes_stats.append(jeu.stats)
    
    print()  # Nouvelle ligne après la progression
    
    # Afficher les résultats; pass the strategies list so the report shows which
    # strategy each player used across all simulated games.
    _afficher_resultats_simulation(resultats, durees, toutes_stats, strategies_for_players, nb_parties)


def _afficher_resultats_simulation(resultats: dict, durees: List[int], 
                                   toutes_stats: List[StatistiquesPartie],
                                   strategies: List[StrategieIA], nb_parties: int):
    """Affiche l'analyse des résultats de simulation"""
    print(f"\n{'='*60}")
    print("ANALYSE DES RÉSULTATS")
    print(f"{'='*60}")
    # If all players used the same strategy, report it simply; otherwise print
    # the per-player mapping used for the simulations.
    try:
        noms_strats = [s.nom for s in strategies]
        unique = set(noms_strats)
        if len(unique) == 1:
            print(f"Stratégie: {noms_strats[0]}")
        else:
            mapping = ", ".join(f"Joueur {i+1} -> {noms_strats[i]}" for i in range(len(noms_strats)))
            print(f"Stratégies par joueur: {mapping}")
    except Exception:
        print("Stratégies: inconnues")
    print(f"Parties jouées: {nb_parties}")
    
    # Taux de victoire
    print(f"\nTaux de victoire:")
    for nom, victoires in sorted(resultats.items(), key=lambda x: x[1], reverse=True):
        # Attach strategy label to player when printing
        try:
            idx = int(nom.split()[1]) - 1
            strat_label = strategies[idx].nom
            label = f"{nom} ({strat_label})"
        except Exception:
            label = nom
        pourcentage = (victoires / nb_parties) * 100
        barre = "█" * int(pourcentage / 2)
        print(f"  {label:32}: {victoires:3}/{nb_parties} ({pourcentage:5.1f}%) {barre}")
    
    # Durée des parties
    print(f"\nDurée des parties:")
    print(f"  Moyenne  : {sum(durees)/len(durees):.1f} tours")
    print(f"  Minimum  : {min(durees)} tours")
    print(f"  Maximum  : {max(durees)} tours")
    print(f"  Médiane  : {sorted(durees)[len(durees)//2]} tours")
    
    # Cases les plus visitées (agrégées)
    print(f"\nTop 5 des cases les plus visitées:")
    passages_total = {}
    for stats in toutes_stats:
        for pos, nb in stats.passages_par_case.items():
            passages_total[pos] = passages_total.get(pos, 0) + nb
    
    if passages_total:
        top_cases = sorted(passages_total.items(), key=lambda x: x[1], reverse=True)[:5]
        total_passages = sum(passages_total.values())
        for pos, nb in top_cases:
            proba = (nb / total_passages) * 100
            print(f"  Position {pos:2}: {proba:5.2f}% des passages")
    
    # Propriétés les plus rentables
    print(f"\nTop 5 des propriétés les plus rentables:")
    revenus_total = {}
    for stats in toutes_stats:
        for nom, rev in stats.revenus_par_propriete.items():
            revenus_total[nom] = revenus_total.get(nom, 0) + rev
    
    if revenus_total:
        top_props = sorted(revenus_total.items(), key=lambda x: x[1], reverse=True)[:5]
        for nom, rev in top_props:
            moyenne = rev / nb_parties
            print(f"  {nom:30}: {moyenne:6.0f}€/partie")


def comparer_strategies(nb_parties: int = 50, nb_joueurs: int = 3):
    """Compare les performances des 3 stratégies d'IA"""
    print("\n" + "="*60)
    print("COMPARAISON DES STRATÉGIES D'IA")
    print("="*60)
    
    strategies = [IAAgressive(), IAConservative(), IAStrategique()]
    resultats_strategies = {}
    
    for strat in strategies:
        print(f"\nTest de la stratégie {strat.nom}...")
        resultats = {f"Joueur {i+1}": 0 for i in range(nb_joueurs)}
        durees = []
        for i in range(nb_parties):
            noms = [f"Joueur {j+1} ({strat.nom})" for j in range(nb_joueurs)]
            jeu = Monopoly(noms, strategie=strat)
            jeu.mode_debug = True

            gagnant = jeu.jouer_partie(max_tours=200)

            if gagnant:
                resultats[gagnant.nom] += 1
            durees.append(jeu.stats.nb_tours)
        
        resultats_strategies[strat.nom] = {
            'victoires': resultats,
            'duree_moyenne': sum(durees) / len(durees) if durees else 0
        }
    
    # Afficher la comparaison
    print(f"\n{'='*60}")
    print("RÉSULTATS COMPARATIFS")
    print(f"{'='*60}")
    
    for nom_strat, data in resultats_strategies.items():
        print(f"\n{nom_strat}:")
        print(f"  Durée moyenne: {data['duree_moyenne']:.1f} tours")
        
        # Équité (écart entre max et min victoires)
        victoires = list(data['victoires'].values())
        equite = max(victoires) - min(victoires)
        print(f"  Équité: écart de {equite} victoires entre joueurs")



def test_complet():
    """Exécute une batterie de tests pour valider le code"""
    print("\n" + "="*60)
    print("BATTERIE DE TESTS")
    print("="*60)
    
    print("\n1. Test du plateau...")
    plateau = Plateau()
    assert len(plateau.cases) == 40, "Le plateau doit avoir 40 cases"
    assert isinstance(plateau.cases[0], CaseSpeciale), "Case 0 = Départ"
    assert isinstance(plateau.cases[5], Gare), "Case 5 = Gare"
    print("   Plateau validé (40 cases)")
    
    print("\n2. Test des joueurs...")
    joueur = Joueur("Test", 1500)
    assert joueur.argent == 1500, "Argent initial incorrect"
    joueur.deplacer(7)
    assert joueur.position == 7, "Déplacement incorrect"
    print("   Joueurs validés")
    
    print("\n3. Test des propriétés...")
    prop = Propriete("Test", 1, 100, 10, "test", 50)
    joueur.acheter_propriete(prop)
    assert prop.proprietaire == joueur, "Achat échoué"
    assert joueur.argent == 1400, "Argent non déduit"
    print("   Propriétés validées")
    
    print("\n4. Test des loyers...")
    joueur2 = Joueur("Test2", 1500)
    loyer = prop.calculer_loyer()
    joueur2.payer(loyer, joueur)
    assert joueur.argent == 1410, "Loyer non reçu"
    print("   Loyers validés")
    
    print("\n5. Test d'une partie courte...")
    jeu = Monopoly(["Alain", "Béa"])
    jeu.mode_debug = True
    for _ in range(5):
        for j in jeu.joueurs:
            if not j.est_en_faillite:
                jeu.jouer_tour(j)
    print("   Partie courte validée")
    
    print("\n" + "="*60)
    print("TOUS LES TESTS RÉUSSIS!")
    print("="*60)



def main():
    """Point d'entrée principal du programme"""
    print("="*60)
    print(" "*15 + "MONOPOLY EN PYTHON")
    print("="*60)
    print("\nQue voulez-vous faire?")
    print("1. Jouer une partie complète (mode automatique)")
    print("2. Jouer une partie interactive")
    print("3. Simuler plusieurs parties")
    print("4. Comparer les stratégies IA")
    print("5. Lancer les tests de validation")
    print("6. Afficher le plateau")
    print("0. Quitter")
    
    choix = _read_int("\n Votre choix (0-6): ", min_val=0, max_val=6)
    
    if choix == 1:
        print("\n" + "="*60)
        # Allow choosing different strategies per player
        print("Voulez-vous utiliser la même stratégie pour tous les joueurs ? (o/n)")
        rep = input("Votre choix (o/n): ").strip().lower()
        available = {
            '1': IAAgressive(),
            '2': IAConservative(),
            '3': IAStrategique()
        }

        if rep == 'n':
            strategies = []
            noms = []
            for i, base_name in enumerate(["Alain", "Béa", "Charles"]):
                print(f"Choisissez la stratégie pour {base_name}:")
                print("  1) Agressive\n  2) Conservative\n  3) Stratégique")
                choice = input(f"Stratégie pour {base_name} (1-3): ").strip()
                strat = available.get(choice, IAStrategique())
                strategies.append(strat)
                noms.append(f"{base_name} ({strat.nom})")
            jeu = Monopoly(noms, strategies)
        else:
            strat = IAStrategique()
            noms = [f"{name} ({strat.nom})" for name in ["Alain", "Béa", "Charles"]]
            jeu = Monopoly(noms, strat)
        jeu.jouer_partie(max_tours=100)
        jeu.stats.afficher_statistiques()
    
    elif choix == 2:
        print("\n" + "="*60)
        nb = _read_int("Nombre de joueurs (2-4): ", min_val=2, max_val=4)
        noms = [input(f"Nom du joueur {i+1}: ") for i in range(nb)]
        jeu = Monopoly(noms, IAStrategique())
        jeu.jouer_partie(max_tours=150, mode_interactif=True)
        jeu.stats.afficher_statistiques()
    
    elif choix == 3:
        print("\n" + "="*60)
        nb_parties = _read_int("Nombre de parties à simuler: ", min_val=1)
        nb_joueurs = _read_int("Nombre de joueurs par partie (2-4): ", min_val=2, max_val=4)
        # default: randomize strategies per player per game
        simuler_parties(nb_parties, nb_joueurs, None)
    
    elif choix == 4:
        print("\n" + "="*60)
        nb_parties = _read_int("Nombre de parties par stratégie: ", min_val=1)
        nb_joueurs = _read_int("Nombre de joueurs par partie (2-4): ", min_val=2, max_val=4)
        comparer_strategies(nb_parties, nb_joueurs)

    elif choix == 5:
        print("\n" + "="*60)
        test_complet()
    
    elif choix == 6:
        print("\n" + "="*60)
        plateau = Plateau()
        plateau.afficher_plateau()
        
    else:
        print("Bye !")

main()


    