from core.interfaces import PromptLoader, AIModel
from typing import Dict, Any, List, Generator

# ==========================================
# 1. LES NOUVELLES BRIQUES (MOCKS)
# ==========================================

class MockPromptLoader(PromptLoader):
    """Charge des prompts depuis la mémoire (pour les tests)"""
    def load_config(self) -> tuple[Dict[str, Any], Dict[str, Any]]:
        print("[LOADER] [MockLoader] Chargement des prompts depuis la memoire RAM...")
        return {}, {"test_mode": "Ceci est un prompt de test"}

class MockAI(AIModel):
    """Une IA qui ne coûte rien et répond instantanément"""
    def analyze(self, images: List[Any], prompt: str, stream: bool = False) -> Generator[str, None, None] | str:
        print(f"[AI] [MockAI] Analyse de {len(images)} image(s) avec le prompt : '{prompt}'")
        return "Analyse simulee terminee avec succes."

# ==========================================
# 2. L'APPLICATION (SIMULÉE)
# ==========================================

def run_app(loader: PromptLoader, ai: AIModel):
    """
    Regarde : cette fonction ne sait PAS qu'elle utilise des Mocks.
    Elle utilise juste les interfaces.
    """
    print("\n--- Demarrage de l'App ---")
    
    # 1. Chargement
    settings, prompts = loader.load_config()
    
    # 2. Utilisation
    prompt_text = prompts.get("test_mode", "Default")
    result = ai.analyze(images=["fake_img.jpg"], prompt=prompt_text)
    
    print(f"[RESULT] Resultat : {result}")

# ==========================================
# 3. LA PREUVE
# ==========================================

if __name__ == "__main__":
    # Scénario : On teste l'évolution sans toucher à l'app
    mon_loader = MockPromptLoader()
    mon_ia = MockAI()
    
    # Injection !
    run_app(mon_loader, mon_ia)
    
    print("\n[SUCCESS] SUCCES : L'architecture est decouplee !")
