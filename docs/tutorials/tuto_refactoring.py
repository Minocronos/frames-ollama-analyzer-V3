# EXEMPLE CONCRET BASÉ SUR TON PROJET (frames-analyzer-V3)
# ---------------------------------------------------------
# Tu m'as demandé comment on aurait pu faire dans ton "PPA" (ton appli).
# Prenons l'exemple de ta base de données (DatabaseManager) dans app.py.

# =========================================================
# 1. LA SITUATION ACTUELLE (SANS INJECTION)
# =========================================================

class DatabaseManager:
    def save_analysis(self, data):
        print(f"[SAVE] SAUVEGARDE REELLE dans history.db : {data}")

# C'est ce que tu as dans app.py (simplifié) :
class GeminiApp_SansInjection:
    def __init__(self):
        # [X] PROBLÈME : L'appli CRÉE elle-même la base de données.
        # Elle est OBLIGÉE d'utiliser la vraie DatabaseManager.
        self.db = DatabaseManager()
    
    def run_analysis(self, data):
        # ... analyse ...
        self.db.save_analysis(data)

# =========================================================
# 2. COMMENT ON AURAIT PU FAIRE (AVEC INJECTION)
# =========================================================

# On change juste une chose : on passe la DB au constructeur !
class GeminiApp_AvecInjection:
    def __init__(self, database):
        # [V] SOLUTION : L'appli UTILISE ce qu'on lui donne.
        # Elle ne sait pas si c'est la vraie DB ou une fausse.
        self.db = database
    
    def run_analysis(self, data):
        self.db.save_analysis(data)

# =========================================================
# 3. POURQUOI C'EST MIEUX ? (LA PREUVE)
# =========================================================

# Imagine tu veux tester ton appli sans polluer ton fichier history.db
# Ou tu veux tester sur un PC qui n'a pas le droit d'écrire sur le disque.

class MockDatabase:
    def save_analysis(self, data):
        print(f"[TEST] TEST : On fait semblant de sauvegarder {data} (Rien n'est écrit sur le disque)")

if __name__ == "__main__":
    print("--- SCENARIO 1 : L'APPLICATION NORMALE ---")
    # Dans ton main.py ou app.py réel :
    vraie_db = DatabaseManager()
    app = GeminiApp_AvecInjection(vraie_db)
    app.run_analysis("Photo de chat")

    print("\n--- SCENARIO 2 : LE TEST (IMPOSSIBLE AVANT) ---")
    # Pour tes tests automatiques :
    fausse_db = MockDatabase()
    app_test = GeminiApp_AvecInjection(fausse_db)
    app_test.run_analysis("Photo de test")
    
    # CONCLUSION :
    # Grâce à l'injection, ton code `GeminiApp` est devenu :
    # 1. Plus flexible (il accepte n'importe quelle DB)
    # 2. Testable (on peut simuler la DB)
    # 3. Plus propre (séparation des responsabilités)
