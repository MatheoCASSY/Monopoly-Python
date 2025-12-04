import mysql.connector


class DB:
    __Proprietes = []

    @classmethod
    def connexionBase(cls):
        mydb = mysql.connector.connect(
            host="localhost",
            user="monopoly_user",   # adapte si besoin
            password="root",        # ton mot de passe
            database="monopoly"
        )
        return mydb

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
                FROM v_proprietes;
            """)

            mesResultats = monCurseur.fetchall()

            for r in mesResultats:
                p = None
                type_code = r["type_propriete_code"]

                try:
                    from src.monopoly_pkg.cases import Propriete, Gare, Compagnie
                except ModuleNotFoundError:
                    try:
                        from monopoly_pkg.cases import Propriete, Gare, Compagnie
                    except Exception:
                        from monopoly import Propriete, Gare, Compagnie

                if type_code == "propriete":
                    p = Propriete(
                        nom=r["nom"],
                        position=r["position"],
                        prix=r["prix_achat"],
                        loyer=r["loyer_base"],
                        couleur=r["couleur"],
                    )

                elif type_code == "gare":
                    p = Gare(
                        nom=r["nom"],
                        position=r["position"]
                    )

                elif type_code == "compagnie":
                    p = Compagnie(
                        nom=r["nom"],
                        position=r["position"],
                        prix=r["prix_achat"]
                    )

                if p is not None:
                    cls.__Proprietes.append(p)

            monCurseur.close()
            maConnexion.close()

        return cls.__Proprietes


if __name__ == '__main__':
    for p in DB.get_proprietes():
        print(f"{p.position} : ({getattr(p, 'couleur', 'n/a')}) {p.nom} - prix d'achat : {p.prix}€")
