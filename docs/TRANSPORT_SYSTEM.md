# 📦 Système de Transport - Résumé

## ✅ Fichiers créés

### Scripts d'automatisation
- **`setup.bat`** - Installation automatique sur nouvelle machine
- **`run.bat`** - Lancement de l'application (déjà existant)
- **`check_env.bat`** - Vérification de l'environnement
- **`export.bat`** - Export automatique en ZIP

### Fichiers de dépendances
- **`requirements.txt`** - Liste des dépendances Python (compatible pip)
- **`pyproject.toml`** - Configuration uv (déjà existant)
- **`uv.lock`** - Verrouillage des versions (déjà existant)

### Documentation
- **`README.md`** - Documentation complète
- **`QUICKSTART.md`** - Guide de démarrage rapide
- **`TRANSPORT_GUIDE.md`** - Guide détaillé de transport

### Configuration
- **`.gitignore`** - Exclusions Git (amélioré)

## 🎯 Workflow de transport

### Méthode 1 : Export ZIP (Plus simple)
```bash
# Machine source
export.bat                    # Crée frames-analyzer-V3-export.zip

# Machine destination
1. Dézipper
2. setup.bat                  # Installe tout
3. run.bat                    # Lance l'app
```

### Méthode 2 : Git (Recommandé pour dev)
```bash
# Machine source
git add .
git commit -m "Update"
git push

# Machine destination
git clone <repo>
cd <repo>
setup.bat
run.bat
```

### Méthode 3 : Copie manuelle
```bash
# Copier TOUT sauf .venv/
# Le .gitignore garantit que .venv n'est jamais inclus dans git

# Machine destination
setup.bat
run.bat
```

## 🔍 Ce qui est automatiquement exclu

Grâce au `.gitignore` amélioré :
- ❌ `.venv/` - Environnement virtuel
- ❌ `__pycache__/` - Cache Python
- ❌ `*.pyc`, `*.pyo` - Bytecode compilé
- ❌ `saved_collections/` - Données utilisateur
- ❌ Fichiers IDE (`.vscode/`, `.idea/`)
- ❌ Fichiers temporaires (`.log`, `.tmp`)
- ❌ Fichiers OS (`Thumbs.db`, `.DS_Store`)

## ⚙️ Ce que fait `setup.bat`

1. ✅ Vérifie Python 3.11+
2. ✅ Installe `uv` si absent
3. ✅ Crée `.venv/` avec `uv venv`
4. ✅ Installe toutes les dépendances depuis `requirements.txt`
5. ✅ Affiche un message de succès

## 📊 Taille du projet

**Avec .venv** : ~500 MB
**Sans .venv** : ~5 MB

Le transport est donc **100x plus léger** !

## 🧪 Test de portabilité

Pour tester sur la même machine :
```bash
# 1. Créer un dossier de test
mkdir E:\test_transport
cd E:\test_transport

# 2. Copier les fichiers (sans .venv)
robocopy "E:\antigravity\frames-analyzer-V3" "E:\test_transport" /E /XD .venv __pycache__ /XF *.pyc *.pyo

# 3. Tester l'installation
setup.bat

# 4. Tester le lancement
run.bat
```

## 🎓 Bonnes pratiques

1. **Toujours utiliser `setup.bat`** sur nouvelle machine
2. **Ne jamais copier `.venv/`** manuellement
3. **Utiliser `export.bat`** pour créer un ZIP propre
4. **Vérifier avec `check_env.bat`** avant installation
5. **Garder `requirements.txt` à jour** avec les nouvelles dépendances

## 🔄 Mise à jour des dépendances

Si tu ajoutes une nouvelle bibliothèque :

```bash
# 1. Installer dans l'environnement actuel
uv pip install nouvelle-lib

# 2. Mettre à jour pyproject.toml
# Ajouter dans la section [project.dependencies]

# 3. Mettre à jour requirements.txt
# Ajouter la ligne : nouvelle-lib>=version

# 4. Synchroniser uv.lock
uv lock
```

## ✨ Avantages du système

- ✅ **Portable** - Fonctionne sur n'importe quelle machine Windows
- ✅ **Léger** - Seulement ~5 MB à transporter
- ✅ **Automatique** - Un seul script pour tout installer
- ✅ **Reproductible** - Mêmes versions partout grâce à uv.lock
- ✅ **Rapide** - uv est beaucoup plus rapide que pip
- ✅ **Simple** - Pas besoin de connaissances techniques

## 📝 Notes

- Le `.venv/` est **toujours** exclu par `.gitignore`
- `uv.lock` garantit les **mêmes versions** partout
- `requirements.txt` assure la **compatibilité pip** si besoin
- Les scripts `.bat` fonctionnent sur **Windows uniquement**
