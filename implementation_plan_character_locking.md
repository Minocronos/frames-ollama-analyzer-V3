# Plan d'Implémentation : Feature "Character Locking" (Verrouillage d'Identité)

## 🎯 Objectif
Permettre à l'utilisateur de "verrouiller" l'identité d'un sujet analysé (ADN Biométrique) pour la réutiliser dans d'autres générations, garantissant ainsi une cohérence parfaite du visage et du corps à travers différents styles (Cyberpunk, Mode, etc.).

## 🏗️ Architecture & Flux de Données

### 1. Le Concept de "Master Identity"
Nous allons introduire un état persistant dans l'application (`st.session_state['master_identity']`) qui stockera le JSON biométrique validé.

### 2. Modifications UI (`app.py`)
*   **Zone d'Analyse Biométrique** :
    *   Ajouter un bouton `💾 Save as Master Identity` après une analyse `biometric_complete` ou `deepstack_biometrics`.
    *   Afficher un indicateur visuel "🔒 Identity Locked" dans la sidebar si une identité est active.
    *   Ajouter un bouton pour effacer/reset l'identité.
*   **Zone de Génération (Autres modes)** :
    *   Détecter si une `master_identity` existe.
    *   Si oui, afficher un toggle "Use Locked Identity" (activé par défaut).

### 3. Modifications Logiciel (`core/`)
*   **Injection de Prompt** :
    *   Modifier la logique de construction du prompt.
    *   Si "Use Locked Identity" est actif :
        *   Injecter le bloc JSON sauvegardé au début du prompt système ou utilisateur.
        *   Instruire l'IA d'utiliser *ces* données précises au lieu de ré-estimer le visage.

## 📝 Étapes d'Implémentation

### Étape 1 : Sauvegarde de l'Identité
*   [x] Dans `app.py`, capturer la sortie de l'analyse biométrique.
*   [x] Parser ou extraire le bloc JSON (ou le texte descriptif complet) de la réponse de l'IA.
*   [x] Stocker ce bloc dans `st.session_state`.

### Étape 2 : Interface Utilisateur
*   [x] Ajouter le bouton de sauvegarde.
*   [x] Ajouter l'indicateur d'état dans la sidebar.

### Étape 3 : Injection dans les Prompts
*   [x] Modifier la fonction qui prépare le prompt final.
*   [x] Créer un template d'injection :
    ```text
    ⚠️ CRITICAL INSTRUCTION: CHARACTER CONSISTENCY
    You must strictly adhere to the following BIOMETRIC DNA for the subject. 
    Do not re-invent facial features. Use these exact specifications:
    
    [INJECTED_JSON_DATA]
    ```

## ✅ Validation
1.  Faire une analyse biométrique sur une photo A.
2.  Verrouiller l'identité.
3.  Lancer une génération "Cyberpunk" sur la photo A (ou même une photo B pour du face-swapping conceptuel ?).
4.  Vérifier que le prompt envoyé contient bien le JSON injecté.
