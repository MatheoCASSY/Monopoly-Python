"""
TP Monopoly - Squelette de code
Durée: 16h sur 4 séances de 4h
"""
from Case import Case  
from Global import TypeCase

class CaseSpeciale(Case):
    """Cases comme Départ, Prison, Taxe, etc."""
    def __init__(self, nom: str, position: int, type_case: TypeCase, montant: int = 0):
        super().__init__(nom, position)
        self.type_case = type_case
        self.montant = montant
    
    def action(self, joueur: 'Joueur', jeu: 'Monopoly'):
        """Action selon le type de case spéciale"""
 
        # Case DEPART
        if self.type_case == TypeCase.DEPART:
            # Recevoir 200€ de bonus (200€ déjà perçu)
            joueur.recevoir(200)
            print(f"    {joueur.nom} reçoit 400€ (case Départ)")

        elif self.type_case == TypeCase.ALLER_PRISON:
            joueur.aller_en_prison()
            print(f"    {joueur.nom} va en prison (case Aller en prison)")

        elif self.type_case == TypeCase.TAXE:
            joueur.payer(self.montant)
            print(f"    {joueur.nom} paye {self.montant} (case Impot / Taxe de luxe)")

        elif self.type_case == TypeCase.PARC_GRATUIT:
            print(f"    {joueur.nom} se repose (case Parc gratuit)")
