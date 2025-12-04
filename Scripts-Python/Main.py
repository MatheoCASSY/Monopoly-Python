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

def simuler_parties(nb_parties: int, nb_joueurs: int, strategie: StrategieIA = None):
    """Simule plusieurs parties et collecte des statistiques agrégées"""
    print(f"\n{'='*60}")
    print(f"SIMULATION DE {nb_parties} PARTIES")
    print(f"{'='*60}")
    
    strategie = strategie or IAAgressive()
    resultats = {f"Joueur {i+1}": 0 for i in range(nb_joueurs)}
    durees = []
    toutes_stats = []
    
    for i in range(nb_parties):
        if (i + 1) % 10 == 0 or i == 0:
            print(f"Progression: {i+1}/{nb_parties}", end='\r')
        
        noms = [f"Joueur {j+1}" for j in range(nb_joueurs)]
        jeu = Monopoly(noms, strategie)
        jeu.mode_debug = True
        
        gagnant = jeu.jouer_partie(max_tours=200)
        
        if gagnant:
            resultats[gagnant.nom] += 1
        durees.append(jeu.stats.nb_tours)
        toutes_stats.append(jeu.stats)
    
    print()  # Nouvelle ligne après la progression
    
    # Afficher les résultats
    _afficher_resultats_simulation(resultats, durees, toutes_stats, strategie, nb_parties)


def _afficher_resultats_simulation(resultats: dict, durees: List[int], 
                                   toutes_stats: List[StatistiquesPartie],
                                   strategie: StrategieIA, nb_parties: int):
    """Affiche l'analyse des résultats de simulation"""
    print(f"\n{'='*60}")
    print("ANALYSE DES RÉSULTATS")
    print(f"{'='*60}")
    print(f"Stratégie: {strategie.nom}")
    print(f"Parties jouées: {nb_parties}")
    
    # Taux de victoire
    print(f"\nTaux de victoire:")
    for nom, victoires in sorted(resultats.items(), key=lambda x: x[1], reverse=True):
        pourcentage = (victoires / nb_parties) * 100
        barre = "█" * int(pourcentage / 2)
        print(f"  {nom:12}: {victoires:3}/{nb_parties} ({pourcentage:5.1f}%) {barre}")
    
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
            noms = [f"Joueur {j+1}" for j in range(nb_joueurs)]
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
    
    choix = input("\n Votre choix (0-6): ").strip()
    
    if choix == "1":
        print("\n" + "="*60)
        noms = ["Alain", "Béa", "Charles"]
        jeu = Monopoly(noms, IAStrategique())
        jeu.jouer_partie(max_tours=100)
        jeu.stats.afficher_statistiques()
    
    elif choix == "2":
        print("\n" + "="*60)
        nb = int(input("Nombre de joueurs (2-4): "))
        noms = [input(f"Nom du joueur {i+1}: ") for i in range(nb)]
        jeu = Monopoly(noms, IAStrategique())
        jeu.jouer_partie(max_tours=150, mode_interactif=True)
        jeu.stats.afficher_statistiques()
    
    elif choix == "3":
        print("\n" + "="*60)
        nb_parties = int(input("Nombre de parties à simuler: "))
        nb_joueurs = int(input("Nombre de joueurs par partie (2-4): "))
        simuler_parties(nb_parties, nb_joueurs, IAStrategique())
    
    elif choix == "4":
        print("\n" + "="*60)
        nb_parties = int(input("Nombre de parties par stratégie: "))
        nb_joueurs = int(input("Nombre de joueurs par partie (2-4): "))
        comparer_strategies(nb_parties, nb_joueurs)

    elif choix == "5":
        print("\n" + "="*60)
        test_complet()
    
    elif choix == "6":
        print("\n" + "="*60)
        plateau = Plateau()
        plateau.afficher_plateau()
        
    else:
        print("Bye !")

main()


    