# Plan de Refactoring : Architecture Évolutive (Dependency Injection)

## 🎯 Objectif
Rendre `frames-analyzer-V3` "Future-Proof".
Tu as dit : *"mon app va évoluer, les prompts vont évoluer, les IA vont évoluer"*.
C'est exactement le cas d'usage où l'Injection de Dépendances devient **rentable**.

Nous allons transformer l'architecture monolithique actuelle en une architecture modulaire.

## 🏗️ Architecture Cible

Nous allons introduire des **Interfaces** (Abstractions) pour les deux piliers qui vont bouger :
1.  **Les Prompts** (Source de données)
2.  **L'Intelligence** (Le modèle IA)

### 1. Gestion des Prompts (`PromptService`)
Actuellement : `app.py` lit directement le fichier YAML.
Cible : `app.py` demande des prompts à un `PromptService`.
*   **Avantage** : Demain, tu pourras charger les prompts depuis une API, une BDD, ou un fichier chiffré sans toucher à `app.py`.

### 2. Gestion des IA (`AIAdapter`)
Actuellement : `GeminiAdapter` est importé et instancié en dur.
Cible : `app.py` utilise une interface `AIModel`.
*   **Avantage** : Tu pourras ajouter `GPT4Adapter`, `ClaudeAdapter`, `LocalLlamaAdapter` et laisser l'utilisateur choisir dans l'UI. L'appli ne verra pas la différence.

### 3. [NOUVEAU] Gestion de la Génération d'Images (`ImageGenerator`)
*   **Futur** : Tu as parlé de **ComfyUI** ou API locale.
*   **Stratégie** : On prépare une interface `ImageGenerator`.
    *   Implémentation 1 : `MockGenerator` (pour tester sans GPU).
    *   Implémentation 2 : `ComfyUIAdapter` (qui appelle ton API locale).
    *   Implémentation 3 : `DalleAdapter` (si besoin).
*   **Bénéfice** : Ton app principale ne saura même pas quel outil génère l'image. Elle dira juste `generator.generate(prompt)`.

## 📝 Étapes de Modification

### Étape 1 : Création des Interfaces (Contrats)
Nous allons créer un fichier `core/interfaces.py` (ou modifier les fichiers existants) pour définir les méthodes obligatoires.

### Étape 2 : Refactoring de la Gestion des Prompts
*   [NEW] Créer `core/prompt_manager.py`
    *   Classe `YamlPromptLoader` (Implémentation actuelle)
*   [MODIFY] `app.py`
    *   Remplacer `load_config()` par l'instanciation de `YamlPromptLoader`.

### Étape 3 : Refactoring de l'Adaptateur IA
*   [MODIFY] `core/gemini_adapter.py`
    *   S'assurer qu'il respecte une structure standard (ex: méthode `analyze(image, prompt)`).
*   [MODIFY] `app.py`
    *   Injecter l'adaptateur choisi au lieu de l'instancier au milieu du code.

## ✅ Validation
Pour vérifier que ça marche :
1.  L'application doit fonctionner **exactement comme avant** (pas de régression).
2.  Nous créerons un petit script `test_evolution.py` qui simulera un changement de source de prompts (ex: charger depuis un dictionnaire en mémoire) pour prouver la flexibilité.
