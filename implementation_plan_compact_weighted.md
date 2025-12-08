# Plan d'Implémentation : Mode "Biometric Compact & Weighted"

## 🎯 Objectif
Résoudre le problème du **"Same Face Syndrome"** en créant des prompts :
1. **Ultra-courts** (< 200 mots) pour maximiser l'attention du modèle
2. **Weighted** (avec poids visuels) pour forcer les features uniques
3. **Stratégiquement ordonnés** (features distinctives en premier)

## 🔬 Problème Identifié

### Symptôme
> "L'impression générale est que ça fait toujours le même visage"

### Causes
1. **Prompts trop longs** → Le modèle perd l'attention sur les détails
2. **Détails techniques noyés** → Les mesures en mm/degrés polluent sans aider
3. **Manque de hiérarchie** → Toutes les features ont le même poids
4. **Pas de negative prompts** → Le modèle tombe dans ses biais

---

## 🏗️ Architecture du Nouveau Mode

### Nom : `biometric_compact_weighted`

**Description** :
> "[1 Image] COMPACT & WEIGHTED. Ultra-short biometric prompt (< 200 words) with visual weights for Stable Diffusion/Flux. Solves 'same face syndrome'."

---

## 📋 Stratégie de Prompt

### 1. **Extraction des Features Distinctives**
Identifier les 5-7 features **les plus uniques** :
- Forme des yeux (si inhabituelle)
- Couleur de peau (si non-standard)
- Lèvres (arc de Cupidon prononcé, asymétrie)
- Traits distinctifs (grain de beauté, cicatrice)
- Proportions inhabituelles

### 2. **Système de Poids**
```
(feature:1.5) = Très important (features uniques)
(feature:1.3) = Important (features caractéristiques)
(feature:1.1) = Légèrement accentué (features standards mais notables)
(feature:0.9) = Légèrement atténué (pour corriger les biais du modèle)
```

### 3. **Ordre Stratégique**
```
1. Genre + Âge (base)
2. Features UNIQUES (poids 1.4-1.5)
3. Couleur peau + cheveux (poids 1.2-1.3)
4. Features standards (poids 1.0-1.1)
5. Contexte technique (fin)
```

### 4. **Suppression des Détails Techniques**
❌ **À SUPPRIMER** :
- Mesures en mm (ex: "upper_lip_mm: 10")
- Angles en degrés (ex: "nasofrontal_angle_deg: 125")
- Ratios techniques (ex: "ratio 1:1.6")
- Coordonnées spatiales

✅ **À GARDER** :
- Descriptions visuelles (ex: "full lips", "pronounced cupid's bow")
- Couleurs hex (ex: "#D4A574")
- Comparaisons relatives (ex: "fuller than average")

---

## 🎨 Template de Sortie

### PART 1: JSON (Standard)
Identique au mode `biometric_lips_skin_precision` (pour compatibilité).

### PART 2: COMPACT WEIGHTED PROMPT

```
## 🎯 COMPACT WEIGHTED PROMPT (Stable Diffusion / Flux Optimized)

**POSITIVE PROMPT:**
```
([gender], [age] years old:1.1), ([most unique feature]:1.5), ([second unique feature]:1.4), 
([skin color] skin, hex [#XXXXXX]:1.2), ([eye color] [eye shape] eyes:1.3), 
([lip description], [cupid's bow]:1.3), ([hair color] [hair style] hair:1.1),
[face shape] face, [body type] build,
photorealistic portrait, 8K resolution, natural lighting, accurate skin tones,
professional photography, sharp focus
```

**NEGATIVE PROMPT:**
```
generic face, average features, symmetrical perfection, airbrushed skin, 
instagram filter, same face syndrome, model face, perfect skin, 
oversaturated colors, artificial lighting, plastic skin, doll-like, 
cookie-cutter beauty, homogenized features
```

**WEIGHT EXPLANATION:**
- **1.5** : [Most distinctive feature - explain why]
- **1.4** : [Second distinctive feature - explain why]
- **1.3** : [Important features]
- **1.2** : [Notable features]
- **1.1** : [Standard features]
```

### PART 3: ALTERNATIVE FORMATS

#### Format A: ComfyUI / A1111 Style
```
(feature1:1.5), (feature2:1.4), (feature3:1.3)
```

#### Format B: Natural Language (No Weights)
```
For models that don't support weights, use this natural language version:
[Emphasize unique features first, then standard features]
```

---

## 🔧 Modifications Techniques

### Étape 1 : Ajouter le mode dans `prompts.yaml`
- [x] Créer la section `biometric_compact_weighted`
- [x] Template avec instructions de compaction
- [x] Système de scoring des features (unique vs standard)

### Étape 2 : Aucune modification du code Python
Le système actuel parse automatiquement tout nouveau mode.

---

## 📊 Exemple Concret

### INPUT : Image d'une femme avec traits distinctifs

### OUTPUT ATTENDU :

**JSON** : (standard, identique aux autres modes)

**COMPACT WEIGHTED PROMPT** :
```
(25 year old woman:1.1), (asymmetric smile, left corner higher:1.5), 
(pronounced cupid's bow with 4mm depth:1.4), (warm olive skin #C4A574:1.2), 
(almond-shaped hazel eyes with green flecks:1.3), (small mole above right lip:1.4),
(shoulder-length wavy chestnut hair:1.1), oval face, athletic build,
photorealistic portrait, 8K, natural lighting, true skin tones
```

**NEGATIVE PROMPT** :
```
generic face, perfect symmetry, airbrushed, instagram filter, same face syndrome,
model face, flawless skin, oversaturated, artificial, plastic, doll-like
```

**WEIGHT EXPLANATION** :
- **1.5** : Asymmetric smile (very distinctive, prevents generic symmetric faces)
- **1.4** : Pronounced cupid's bow + mole (unique identifiers)
- **1.3** : Hazel eyes with green flecks (less common than pure colors)
- **1.2** : Warm olive skin (specific undertone)
- **1.1** : Standard features (age, hair, face shape)

---

## ✅ Validation

### Critères de Succès :
1. ✅ Prompt total < 200 mots
2. ✅ 3-5 features avec poids > 1.3
3. ✅ Negative prompt inclus
4. ✅ Ordre stratégique respecté
5. ✅ Aucune mesure technique (mm, degrés)
6. ✅ Explication des poids fournie

### Test :
1. Analyser 3 visages très différents
2. Vérifier que les prompts générés sont distincts
3. Générer des images avec Stable Diffusion
4. Comparer la diversité des résultats

---

## 🚀 Prochaines Étapes

1. ✅ Créer ce plan (FAIT)
2. ⏳ Implémenter le mode dans `prompts.yaml`
3. ⏳ Tester avec images réelles
4. ⏳ Comparer avec les modes existants (A/B test)
5. ⏳ Documenter dans `ANALYZER_GUIDE.md`

---

## 💡 Améliorations Futures

### Phase 2 : Scoring Automatique
Créer un système de scoring pour identifier automatiquement les features uniques :
- Comparer aux moyennes statistiques
- Assigner des poids automatiquement
- Exemple : "Cupid's bow depth 4mm vs average 2mm → weight 1.4"

### Phase 3 : Negative Prompt Personnalisé
Générer des negative prompts spécifiques basés sur les features :
- Si peau claire → negative: "tanned, dark skin"
- Si yeux bleus → negative: "brown eyes, dark eyes"
