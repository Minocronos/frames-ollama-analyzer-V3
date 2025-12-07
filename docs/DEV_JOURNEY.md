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

*À suivre...*
