# Product Requirements Document (PRD): Gemini-3-Streamlit-App

<!-- 
COMMENTAIRE DU DÉVELOPPEUR (Antigravity):
J'ai réécrit ce PRD pour tirer parti des forces spécifiques de Gemini 3 :
1. **Multimodalité native** : Gemini 3 excelle à comprendre la vidéo et le texte simultanément. J'ai donc simplifié le pipeline d'analyse pour envoyer des séquences d'images directement au modèle plutôt que de faire trop de pré-traitement.
2. **Raisonnement complexe** : J'ai ajouté des modes d'analyse "Chain-of-Thought" pour que le modèle explique son processus créatif.
3. **Interface Streamlit** : Pour la rapidité d'itération et la flexibilité du design (CSS custom), comme demandé.
-->

## 1. Vision & Objectifs
Créer une application **"Bold & Premium"** qui utilise **Gemini 3 Pro Preview** (via Ollama) pour transformer l'analyse vidéo en art. L'application doit être visuellement époustouflante, rapide à itérer (hot-reload des prompts), et techniquement robuste.

### Pourquoi Gemini 3 ?
Contrairement aux modèles précédents, Gemini 3 possède une fenêtre de contexte massive et une capacité de raisonnement supérieure. Nous allons l'utiliser pour :
- Comprendre la narration temporelle d'une vidéo (pas juste image par image).
- Générer des prompts de génération vidéo (pour Runway, Luma, Kling, Veo 3) extrêmement détaillés et cohérents.

## 2. Architecture Technique

### Stack
- **Frontend**: Streamlit (avec Custom CSS pour le look "Premium").
- **Backend IA**: Ollama (Support multi-modèles).
- **Gestionnaire de Paquets**: `uv` (pour la rapidité et la propreté).
- **Traitement Vidéo**: OpenCV (extraction de frames).

### Flux de Données (Data Flow)
1.  **Input**: Utilisateur upload une vidéo.
2.  **Processing**: Extraction intelligente des frames (par intervalle ou par nombre).
3.  **Selection**: Utilisateur sélectionne les frames à analyser (désélectionnées par défaut).
4.  **Reasoning (Gemini 3)**:
    -   *Mode Analyse*: "Que se passe-t-il dans cette séquence ?"
    -   *Mode Créatif*: "Réimagine cette scène dans le style Cyberpunk Noir."
5.  **Output**: Description textuelle, Prompt pour Générateur Vidéo, ou Analyse structurée.

## 3. Fonctionnalités Implémentées ✅

### A. Extraction & Sélection de Frames
-   **Stratégies multiples**: Par intervalle (secondes) ou par nombre total
-   **Valeurs par défaut**: 2 secondes / 50 frames
-   **Sélection intelligente**: 
    -   Frames **désélectionnées par défaut** après extraction
    -   Boutons "Select All" / "Deselect All"
    -   Grille visuelle 4 colonnes avec checkboxes
    -   Compteur de sélection en temps réel

### B. Interface Utilisateur Premium
-   **Design Dark Mode**: Fond #0E1117, accents gradient (FF4B4B → FF914D)
-   **Typographie**: Inter/Roboto avec letterspacing optimisé
-   **Animations**: Hover effects, transitions fluides
-   **Activity Log**: Sidebar avec suivi en temps réel des actions
-   **Pipeline Visualization**: Graphe Mermaid dynamique

### C. Système d'Analyse Multi-Modes
-   **Technical Analysis**: Lumière, composition, mouvement caméra
-   **Creative Conversion**: Transformation artistique avec styles prédéfinis
-   **Video Prompt Generation**: Prompts optimisés pour Runway, Luma, Kling, Veo 3
-   **Descriptions contextuelles**: Chaque mode expliqué dans l'UI

### D. Bibliothèque de Styles Créatifs
-   **Cinématiques**: Film Noir, Cyberpunk, Wes Anderson
-   **3D/CGI**: Pixar, Unreal Engine 5, Claymation
-   **Fashion**: Vogue Editorial, Haute Couture
-   **Artistiques**: Impressionniste, Surréaliste, Hyper-réaliste
-   **Expérimentaux**: Glitch Art, Datamosh, VHS Aesthetic

### E. Support Multi-Modèles
-   **Ollama**: Détection automatique des modèles installés
-   **Fallback intelligent**: Utilise settings.yaml si erreur
-   **Sélection dynamique**: Dropdown avec modèles disponibles

## 4. Configuration & Extensibilité
Tout est configurable sans toucher au code Python :
-   **`config/prompts.yaml`**: Templates Jinja2, modes d'analyse, styles, descriptions
-   **`config/settings.yaml`**: Modèle par défaut, température, max tokens
-   **Hot-Reload**: Modifications visibles instantanément

## 5. Architecture Actuelle

### Structure du Projet
```
├── app.py                  # Application Streamlit principale
├── core/
│   ├── video_processor.py  # Extraction de frames (OpenCV)
│   └── gemini_adapter.py   # Interface Ollama avec streaming
├── ui/
│   └── components.py       # Graphe Mermaid, composants réutilisables
├── config/
│   ├── prompts.yaml        # Templates et styles
│   └── settings.yaml       # Configuration modèle
└── run.bat                 # Lanceur avec venv activation
```

### Flux de Données Détaillé
1. **Upload** → Vidéo uploadée via Streamlit file_uploader
2. **Extract** → Frames extraites (stratégie configurable: interval/count)
3. **Select** → Utilisateur choisit les frames (désélectionnées par défaut)
4. **Analyze** → Envoi à Ollama avec prompt template (Jinja2)
5. **Stream** → Réponse affichée en temps réel avec cursor animé

## 6. Prochaines Évolutions Possibles
-   [ ] Export des résultats (JSON, Markdown)
-   [ ] Historique des analyses
-   [ ] Comparaison multi-modèles (side-by-side)
-   [ ] Batch processing de plusieurs vidéos
-   [ ] API REST pour intégration externe
-   [ ] Détection automatique de scènes (scene detection)

---
*Dernière mise à jour: 2025-11-20 | Status: Production-Ready*