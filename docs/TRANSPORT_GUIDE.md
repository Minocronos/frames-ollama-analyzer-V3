# Transport Checklist - Artidicia

## 📦 Avant de transporter

### Fichiers à INCLURE
- ✅ Tous les fichiers `.py`
- ✅ `config/` (prompts.yaml)
- ✅ `core/` (modules Python)
- ✅ `ui/` (composants)
- ✅ `requirements.txt`
- ✅ `pyproject.toml`
- ✅ `uv.lock`
- ✅ `setup.bat`
- ✅ `run.bat`
- ✅ `check_env.bat`
- ✅ `README.md`
- ✅ `.gitignore`
- ✅ `.python-version`
- ✅ Fichiers de documentation (*.md, *.png)

### Fichiers à EXCLURE
- ❌ `.venv/` (sera recréé)
- ❌ `__pycache__/` (sera recréé)
- ❌ `*.pyc`, `*.pyo` (sera recréé)
- ❌ `saved_collections/` (optionnel - données utilisateur)

## 🚀 Sur la nouvelle machine

### Étape 1 : Vérification
```bash
check_env.bat
```
Vérifie que Python 3.11+ est installé.

### Étape 2 : Installation
```bash
setup.bat
```
Installe tout automatiquement :
- uv (si absent)
- Environnement virtuel
- Toutes les dépendances

### Étape 3 : Lancement
```bash
run.bat
```

## 🔄 Méthodes de transport

### Méthode 1 : ZIP (Simple)
1. Supprimer `.venv/` si présent
2. Zipper tout le dossier
3. Dézipper sur nouvelle machine
4. Exécuter `setup.bat`

### Méthode 2 : Git (Recommandé)
```bash
# Machine source
git add .
git commit -m "Update"
git push

# Machine destination
git clone <repo>
cd <repo>
setup.bat
```

### Méthode 3 : Copie réseau/USB
1. Copier le dossier (`.venv` sera ignoré automatiquement si vous utilisez robocopy)
2. Sur nouvelle machine : `setup.bat`

## 📋 Commande robocopy (Windows)
```bash
robocopy "E:\antigravity\frames-analyzer-V3" "D:\destination" /E /XD .venv __pycache__ /XF *.pyc *.pyo
```

## ✅ Vérification post-installation

Après `setup.bat`, vérifiez :
1. `.venv/` existe
2. `run.bat` lance Streamlit sans erreur
3. L'app s'ouvre dans le navigateur

## 🐛 Si problème

1. Supprimer `.venv/`
2. Relancer `setup.bat`
3. Vérifier les logs d'erreur
4. S'assurer que Python 3.11+ est dans le PATH
