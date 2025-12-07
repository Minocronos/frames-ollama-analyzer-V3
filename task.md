# Tâches de Refactoring (Injection de Dépendances)

- [x] **Étape 1 : Création des Interfaces** <!-- id: 0 -->
    - [x] Créer `core/interfaces.py` (PromptLoader, AIModel, ImageGenerator) <!-- id: 1 -->
- [x] **Étape 2 : Gestion des Prompts** <!-- id: 2 -->
    - [x] Créer `core/prompt_manager.py` (Implémentation YamlPromptLoader) <!-- id: 3 -->
    - [x] Modifier `app.py` pour utiliser `YamlPromptLoader` <!-- id: 4 -->
- [x] **Étape 3 : Gestion de l'IA** <!-- id: 5 -->
    - [x] Adapter `core/gemini_adapter.py` à l'interface `AIModel` <!-- id: 6 -->
    - [x] Injecter l'adaptateur dans `app.py` <!-- id: 7 -->
- [x] **Étape 4 : Validation** <!-- id: 8 -->
    - [x] Vérifier que l'application démarre et fonctionne <!-- id: 9 -->
    - [x] Créer un script de démonstration `test_evolution.py` <!-- id: 10 -->
