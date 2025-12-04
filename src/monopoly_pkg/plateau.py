from typing import List

def _import_DB():
    try:
        from src.db import DB
    except ModuleNotFoundError:
        from db import DB
    return DB

from .cases import Case, CaseSpeciale, TypeCase


class Plateau:
    def __init__(self):
        self.cases: List[Case] = []
        self._creer_plateau()

    def _creer_plateau(self):
        DB = _import_DB()
        self.cases = [None] * 40
        self.cases[0] = CaseSpeciale("Départ", 0, TypeCase.DEPART)
        self.cases[2] = CaseSpeciale("Caisse de Communauté", 2, TypeCase.CAISSE_DE_COMMUNAUTE)
        self.cases[4] = CaseSpeciale("Impot sur le revenu", 4, TypeCase.TAXE)
        self.cases[7] = CaseSpeciale("Chance", 7, TypeCase.CHANCE)
        self.cases[10] = CaseSpeciale("Prison", 10, TypeCase.PRISON)
        self.cases[17] = CaseSpeciale("Caisse de Communauté", 17, TypeCase.CAISSE_DE_COMMUNAUTE)
        self.cases[20] = CaseSpeciale("Parc Gratuit", 20, TypeCase.PARC_GRATUIT)
        self.cases[22] = CaseSpeciale("Chance", 22, TypeCase.CHANCE)
        self.cases[30] = CaseSpeciale("Allez en Prison", 30, TypeCase.ALLEZ_PRISON)
        self.cases[33] = CaseSpeciale("Caisse de Communauté", 33, TypeCase.CAISSE_DE_COMMUNAUTE)
        self.cases[36] = CaseSpeciale("Chance", 36, TypeCase.CHANCE)
        self.cases[38] = CaseSpeciale("Taxe de Luxe", 38, TypeCase.TAXE)

        for p in DB.get_proprietes():
            self.cases[p.position] = p

    def get_case(self, position: int) -> Case:
        return self.cases[position % len(self.cases)]
