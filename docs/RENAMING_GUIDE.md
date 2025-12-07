# 📝 GUIDE DE RENOMMAGE - ÉTAPES À SUIVRE

## ✅ Modifications déjà faites

- ✅ `pyproject.toml` - Nom du projet mis à jour

## 🔄 ÉTAPES DE RENOMMAGE

### Étape 1 : Fermer VS Code
**IMPORTANT** : Ferme complètement VS Code pour déverrouiller le dossier.

---

### Étape 2 : Renommer le dossier

**Option A - Explorateur Windows (Recommandé) :**
1. Ouvre l'explorateur Windows
2. Va dans `E:\antigravity\`
3. Clique droit sur `test1`
4. Sélectionne "Renommer"
5. Tape : `frames-analyzer-V3`
6. Appuie sur Entrée

**Option B - PowerShell :**
```powershell
cd E:\antigravity
Rename-Item -Path "test1" -NewName "frames-analyzer-V3"
```

---

### Étape 3 : Rouvrir VS Code

1. Ouvre VS Code
2. File → Open Folder
3. Sélectionne `E:\antigravity\frames-analyzer-V3`

---

### Étape 4 : Vérification

Vérifie que tout fonctionne :

```bash
# Dans le nouveau dossier
run.bat
```

Si l'app démarre correctement, c'est bon ! ✅

---

### Étape 5 : Git (si tu utilises Git)

**Pas de panique !** Git gère parfaitement les renommages.

```bash
# 1. Vérifier le statut (Git détecte le renommage automatiquement)
git status

# 2. Ajouter tous les changements
git add -A

# 3. Commit
git commit -m "Rename project to frames-analyzer-V3"

# 4. Push (si tu as un remote)
git push
```

**Voir `GIT_RENAMING.md` pour plus de détails.**

---

## 📋 Checklist

- [ ] VS Code fermé
- [ ] Dossier renommé de `test1` → `frames-analyzer-V3`
- [ ] VS Code rouvert dans le nouveau dossier
- [ ] `run.bat` fonctionne
- [ ] (Optionnel) Supprimer ce fichier `RENAMING_GUIDE.md`

---

## 🎯 Nouveau chemin

**Ancien :** `E:\antigravity\test1`  
**Nouveau :** `E:\antigravity\frames-analyzer-V3`

---

## ⚠️ Note importante

Si tu utilises Git, après le renommage :

```bash
# Git détectera automatiquement le renommage
git status
git add .
git commit -m "Rename project to frames-analyzer-V3"
```

---

**Une fois terminé, tout sera prêt ! 🚀**
