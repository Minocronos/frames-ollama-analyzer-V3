# 🔧 Scripts Utilitaires

Ce dossier contient les scripts pour gérer l'installation et le transport de l'application.

## 📋 Scripts Disponibles

### `setup.bat` - Installation
Installe automatiquement l'environnement sur une nouvelle machine.

**Usage :**
```bash
scripts\setup.bat
```

**Ce qu'il fait :**
1. Vérifie Python 3.11+
2. Installe `uv` si nécessaire
3. Crée l'environnement virtuel `.venv`
4. Installe toutes les dépendances

---

### `export.bat` - Export
Crée un fichier ZIP prêt à transporter.

**Usage :**
```bash
scripts\export.bat
```

**Résultat :**
- Crée `frames-analyzer-V3-export.zip` à la racine
- Exclut automatiquement `.venv/`, `__pycache__/`, etc.
- Prêt à copier sur autre machine

---

### `check_env.bat` - Vérification
Vérifie que l'environnement est correctement configuré.

**Usage :**
```bash
scripts\check_env.bat
```

**Vérifie :**
- Python installé
- uv installé
- `.venv` existe
- Fichiers de dépendances présents

---

## 🎯 Workflow Typique

### Sur cette machine
```bash
# Juste lancer l'app
run.bat
```

### Pour transporter
```bash
# 1. Créer l'export
scripts\export.bat

# 2. Copier frames-analyzer-V3-export.zip

# 3. Sur autre machine : dézipper puis
scripts\setup.bat

# 4. Lancer
run.bat
```

---

**Retour à la racine** → `cd ..`
