# 🎓 Mon Journal de Dév (Concepts Appris)

Ce fichier résume les concepts techniques que nous avons abordés ensemble. C'est votre base de connaissances pour devenir un meilleur développeur.

---

## 📅 Session : Base de Données & UI (27/11/2025)

### 1. La Base de Données (SQLite)
**C'est quoi ?**
Un fichier unique (`history.db`) qui agit comme un tableau Excel invisible et super rapide.

**Pourquoi on l'utilise ?**
Pour ne pas perdre les prompts générés et pouvoir les trier/filtrer plus tard (ce qu'on ne peut pas faire avec des fichiers texte en vrac).

**Le Code Clé (`core/database.py`) :**
```python
# Créer une table (une feuille Excel)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS analyses (
        id INTEGER PRIMARY KEY,  -- Numéro unique
        prompt_content TEXT,     -- Le texte à sauver
        rating INTEGER           -- La note (étoiles)
    )
''')
```

### 2. L'Interface Utilisateur (Streamlit Columns)
**Le Problème :**
Les étoiles de notation s'affichaient sur deux lignes parce que la colonne était trop étroite.

**La Solution :**
On a joué avec les proportions des colonnes.
```python
# Avant (Trop serré)
c1, c2, c3 = st.columns([1, 2, 1]) 
# 1 part pour les étoiles, 2 parts pour le commentaire

# Après (Plus large)
c1, c2, c3 = st.columns([2, 3, 1])
# 2 parts pour les étoiles -> Elles ont la place de s'étaler !
```

### 3. Le Concept RLHF (Reinforcement Learning from Human Feedback)
**C'est quoi ?**
C'est quand l'humain (vous) note le travail de l'IA.

**Pourquoi c'est puissant ?**
Au lieu de juste *utiliser* l'IA, vous *créez de la valeur*.
- **Prompt sans note** = Juste du texte.
- **Prompt + 5 étoiles** = Une vérité terrain ("Ground Truth"). C'est ça qui permet d'entraîner une IA à avoir votre "goût".

---

## 📅 Session : Fusion Intelligente & Character Locking (07/12/2025)

### 1. Le Problème de la "Fusion Aveugle"
**Le Problème :**
Dans l'interface, l'utilisateur choisit "Focus: Face" pour l'image A et "Focus: Body" pour l'image B.
Mais le code envoyait juste les deux images à l'IA sans lui expliquer ces rôles. L'IA faisait une "moyenne" floue.

**La Solution (Injection de Contexte) :**
On a modifié `app.py` pour traduire les choix de l'UI en instructions textuelles pour le prompt.

**Le Code Clé (`app.py`) :**
```python
# On construit une "Carte des Rôles"
if focus == "Character/Face":
    instruction = "(STRICTLY EXTRACT FACE. IGNORE CLOTHING.)"
elif focus == "Clothing":
    instruction = "(STRICTLY EXTRACT OUTFIT. IGNORE FACE.)"

# On l'injecte dans le prompt final
prompt_text = f"""
USER ASSIGNED ROLES:
- Image 1: {instruction_1}
- Image 2: {instruction_2}

PRIORITY RULE:
If Image 1 is 'Face', use ONLY Image 1 for facial features.
""" + prompt_text
```

### 2. Le Concept de "Character Locking" (Verrouillage d'Identité)
**L'Objectif :**
Garder le même visage exactement sur 50 générations différentes (Cyberpunk, Mode, etc.).

**L'Architecture "Master Identity" :**
1.  **Analyse** : On fait un scan biométrique complet (`biometric_complete`).
2.  **Stockage** : On sauvegarde le résultat JSON dans la mémoire de session (`st.session_state['master_identity']`).
3.  **Injection** : Pour les générations suivantes, on force l'IA à utiliser ce JSON comme "Vérité Absolue".

**Pourquoi c'est mieux que le "Fine-tuning" ?**
C'est instantané (pas d'entraînement), gratuit, et flexible (on peut éditer le JSON à la main).

---


## 📅 Session : Persistence & Stabilité (07/12/2025)

### 1. La Persistance d'État (`st.session_state`)
**Le Problème :**
Quand on cliquait sur "LOCK", la page se rechargeait (`st.rerun()`) et tout disparaissait (le résultat de l'analyse, le bouton lock, etc.). C'est le comportement par défaut de Streamlit.

**La Solution :**
On a découplé l'analyse de l'affichage.
1.  **Au clic sur "Analyze"** : On fait le travail et on *sauvegarde* tout dans `st.session_state['current_result']`.
2.  **Au chargement de la page** : On vérifie si `current_result` existe. Si oui, on l'affiche.
Cela permet à l'affichage de survivre aux rechargements de page déclenchés par d'autres boutons (comme le Lock).

### 2. L'Indentation Python
**La Leçon Douloureuse :**
Python est impitoyable avec les espaces. Un mélange de blocs copiés-collés à différents niveaux d'imbrication (dans des `if`, des `try`, des `with`) a causé des `IndentationError` en cascade.
**Règle d'or :** Toujours vérifier l'alignement vertical strict des blocs logiques.

### 3. Interception de Flux (Streaming)
**Le Besoin :**
L'utilisateur voulait voir et verrouiller le JSON *pendant* que l'IA continuait d'écrire le reste du texte, sans attendre la fin.

**La Technique (Évolution) :**
Initialement, on utilisait des Regex complexes. Ça échouait souvent.
**Solution Finale :** "Brute Force". On cherche simplement la première `{` et la dernière `}` dans le flux. On essaie de parser. Si ça marche, on affiche.
C'est beaucoup plus robuste et rapide que d'essayer de deviner le format exact du Markdown.
Cela crée une interface ultra-réactive où le contrôle (Lock) apparaît avant même que l'analyse soit finie.

---

*À suivre...*
