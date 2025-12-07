# EXEMPLE : POURQUOI L'INJECTION DE DÉPENDANCES EST UTILE (Même pour un Junior)

# ---------------------------------------------------------
# [X] MAUVAISE FAÇON (Couplage fort)
# C'est ce qu'on fait souvent quand on débute.
# ---------------------------------------------------------

class VraieBaseDeDonnees:
    def lire(self):
        # Imagine que ça se connecte à un vrai serveur SQL lent
        print("[CONNEXION] Connexion à la VRAIE base de données (c'est lent)...")
        return "Données secrètes"

class AnalyseurJunior:
    def __init__(self):
        # PROBLÈME : L'Analyseur crée lui-même la base de données.
        # Il est "marié" avec VraieBaseDeDonnees. Impossible de changer sans casser le code.
        self.db = VraieBaseDeDonnees()
    
    def analyser(self):
        data = self.db.lire()
        return f"Analyse de : {data}"

# ---------------------------------------------------------
# [V] BONNE FAÇON (Injection de Dépendances)
# C'est le principe de FastAPI, Angular, etc.
# ---------------------------------------------------------

class AnalyseurPro:
    # MAGIE : On demande la base de données en argument (Injection).
    # L'Analyseur s'en fiche de savoir d'où elle vient, tant qu'elle a une méthode .lire()
    def __init__(self, base_de_donnees):
        self.db = base_de_donnees

    def analyser(self):
        data = self.db.lire()
        return f"Analyse de : {data}"

# ---------------------------------------------------------
# [TEST] POURQUOI C'EST GÉNIAL POUR LES TESTS ?
# ---------------------------------------------------------

# Imagine tu veux tester ton code sans internet ou sans casser la vraie base.
# Tu crées une "Fausse" base juste pour le test.

class FausseBasePourTest:
    def lire(self):
        print("[TEST] Utilisation d'une fausse base (rapide et sûr)")
        return "Données de test"

if __name__ == "__main__":
    print("--- Test Junior (Obligé d'utiliser la vraie base) ---")
    app_junior = AnalyseurJunior()
    print(app_junior.analyser())
    
    print("\n--- Test Pro (On peut choisir sa base !) ---")
    # C'est ici qu'on fait l'injection : on "injecte" la fausse base
    ma_fausse_db = FausseBasePourTest()
    app_pro = AnalyseurPro(ma_fausse_db) 
    print(app_pro.analyser())
