# 🚀 QUICK START - Artidicia

## Sur CETTE machine (déjà configurée)
```bash
run.bat
```

## Sur une NOUVELLE machine

### Option 1 : Export automatique (Recommandé)
```bash
# Sur cette machine
export.bat              # Crée un ZIP

# Sur nouvelle machine
1. Dézipper
2. setup.bat           # Installation auto
3. run.bat             # Lancement
```

### Option 2 : Copie manuelle
```bash
# Copier tout SAUF .venv/

# Sur nouvelle machine
setup.bat              # Installation auto
run.bat                # Lancement
```

## 🔧 Scripts disponibles

| Script          | Description                              |
| --------------- | ---------------------------------------- |
| `run.bat`       | Lance l'application                      |
| `setup.bat`     | Installation complète (nouvelle machine) |
| `check_env.bat` | Vérifie l'environnement                  |
| `export.bat`    | Crée un ZIP pour transport               |

## 📋 Prérequis nouvelle machine
- Python 3.11+ installé
- C'est tout ! `setup.bat` fait le reste

## ❓ Problème ?
Voir `TRANSPORT_GUIDE.md` ou `README.md`
