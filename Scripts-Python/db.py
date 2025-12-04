# Pour installer le connecteur mysql, dans la fenetre terminal :
# python -m pip install --user mysql-connector-python
import mysql.connector

from Propriete import Propriete
from Gare import Gare
from Compagnie import Compagnie

class DB:
    @classmethod
    def connexionBase(cls):
        mydb = mysql.connector.connect(
          host="localhost",
          user="monopoly_user",
          password="Azerty$",
          database = "monopoly"
        )
        return mydb

# TABLE PROPRIETES -------------------------------------------------------

# Liste des proprietes. donnée de classe
    __Proprietes = []
    
    @classmethod
    def get_proprietes(cls):
        if cls.__Proprietes == []:
            maConnexion = cls.connexionBase()
            monCurseur = maConnexion.cursor(dictionary=True)
 
            monCurseur.execute("""
                SELECT position,
                       nom,
                       type_propriete_code,
                       prix_achat,
                       loyer_base,
                       couleur,
                       prix_maison
                FROM   v_proprietes;""")
            mesResultats = monCurseur.fetchall()

            for r in mesResultats:
                p = None
                if r["type_propriete_code"] == "propriete":           
                    # je cree une propriete
                    p = Propriete(r["nom"], int(r["position"]), int(r["prix_achat"]), int(r["loyer_base"]), r["couleur"], int(r["prix_maison"]))
                elif r["type_propriete_code"] == "gare":
                    # je cree une Gare
                    p = Gare(r["nom"], int(r["position"]))
                elif r["type_propriete_code"] == "compagnie":
                    p = Compagnie(r["nom"], int(r["position"]))

                if p is not None:
                    cls.__Proprietes.append(p)
            
        return cls.__Proprietes
    
# test
if __name__ == '__main__':
    for p in DB.get_proprietes():
        print(f"{p.position} : ({p.couleur}) {p.nom} - prix d'achat : {p.prix}€")



        
