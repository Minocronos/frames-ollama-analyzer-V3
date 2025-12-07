# 🔄 GIT ET RENOMMAGE - PAS DE PROBLÈME !

## ✅ Git gère automatiquement les renommages

Quand tu renommes un dossier, Git détecte automatiquement que c'est un **renommage**, pas une suppression + création.

---

## 📋 COMMANDES GIT APRÈS RENOMMAGE

### Étape 1 : Vérifier le statut
```bash
git status
```

**Tu verras :**
```
renamed:    (ancien chemin) -> (nouveau chemin)
```

Git détecte automatiquement le renommage ! ✅

---

### Étape 2 : Ajouter les changements
```bash
git add .
```

Ou plus précis :
```bash
git add -A
```

Le flag `-A` capture tous les changements incluant les renommages.

---

### Étape 3 : Commit
```bash
git commit -m "Rename project from test1 to frames-analyzer-V3"
```

---

### Étape 4 : Push (si tu as un remote)
```bash
git push
```

---

## 🎯 WORKFLOW COMPLET

```bash
# 1. Après avoir renommé le dossier
cd E:\antigravity\frames-analyzer-V3

# 2. Vérifier
git status

# 3. Ajouter tout
git add -A

# 4. Commit
git commit -m "Rename project to frames-analyzer-V3"

# 5. Push (si nécessaire)
git push
```

---

## ⚠️ IMPORTANT

### Si tu as un dépôt distant (GitHub, GitLab, etc.)

**Option 1 : Garder le même dépôt (Recommandé)**
- Le renommage local n'affecte PAS le nom du dépôt distant
- Tu peux avoir un dossier local `frames-analyzer-V3` et un repo GitHub `test1`
- Aucun problème !

**Option 2 : Renommer aussi le dépôt distant**
- Va sur GitHub/GitLab
- Settings → Rename repository
- Puis mets à jour l'URL remote :
  ```bash
  git remote set-url origin <nouvelle-url>
  ```

---

## 🔍 VÉRIFICATION

Après le commit, vérifie l'historique :
```bash
git log --oneline --name-status -1
```

Tu verras :
```
R100    ancien/chemin -> nouveau/chemin
```

Le `R100` signifie "Rename à 100%" - Git a bien compris ! ✅

---

## 💡 POURQUOI ÇA FONCTIONNE ?

Git ne stocke **PAS** les fichiers par leur chemin, mais par leur **contenu** (hash SHA).

Quand tu renommes :
- Le contenu ne change pas
- Git détecte que c'est le même contenu à un nouvel emplacement
- Il enregistre ça comme un renommage, pas une suppression + création

---

## 🎉 CONCLUSION

**AUCUN PROBLÈME avec Git !**

Juste :
1. Renomme le dossier
2. `git add -A`
3. `git commit -m "Rename project"`
4. `git push`

C'est tout ! 🚀

---

## 📝 NOTE

Si tu veux être sûr à 100%, fais un backup avant :
```bash
# Optionnel : créer une branche de backup
git branch backup-before-rename
```

Mais ce n'est vraiment pas nécessaire, Git gère ça parfaitement ! ✅
