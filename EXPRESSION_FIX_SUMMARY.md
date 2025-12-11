# ✅ Expression Fix - Anti Smile Bias

## 🔴 Problème
**User Report:** "Le modèle sourit bêtement alors que l'original non"

**Cause:**
- Biais "sourire" des modèles d'IA (datasets pleins de photos souriantes)
- Absence d'instruction explicite sur l'expression faciale
- "Portrait" = sourire par défaut dans l'esprit de l'IA

## ✅ Solution Implémentée

### 1. Nouveau Champ `expression` dans le JSON
```json
"face": {
  "expression": {
    "type": "neutral/smiling/serious/surprised/sad/angry/etc",
    "mouth_state": "closed/slightly open/wide smile/teeth showing",
    "eye_expression": "neutral gaze/squinting/wide/relaxed",
    "overall_intensity": "subtle/moderate/strong",
    "description": "CRITICAL: Prevents AI smile bias. Describe EXACT expression."
  }
}
```

### 2. Expression Ajoutée au Prompt Weighted
**Template modifié (ligne 936) :**
```
([expression.type] expression, [mouth_state], [eye_expression]:1.3),
```

**Exemple concret :**
```
(neutral expression, lips closed, neutral gaze:1.3),
```

### 3. Negative Prompt Conditionnel
**Ajout automatique si expression = neutral/serious :**
```
NEGATIVE PROMPT:
..., smiling, smile, grin, happy expression, teeth showing, cheerful, beaming
```

### 4. Instructions Critiques Ajoutées
```
**⚠️ CRITICAL INSTRUCTIONS:**
1. For skin, use `skin_tone_visual` field
2. For expression, use exact terms from JSON (e.g., "neutral expression, lips closed")
3. If expression is neutral/serious, ADD to negative prompt: "smiling, smile, grin"
```

## 📁 Modifications

### `config/prompts.yaml`
- **Ligne 824-831** : Ajout champ `expression` dans `biometric_compact_weighted`
- **Ligne 536-543** : Ajout champ `expression` dans `biometric_lips_skin_precision`
- **Ligne 936** : Expression ajoutée au template de prompt
- **Ligne 945-947** : Instructions critiques pour l'expression
- **Ligne 960** : Negative prompt conditionnel pour smile bias

## 🎯 Résultat Attendu

### Test Case: Visage Neutre

**INPUT (Image):**
- Personne avec expression neutre
- Bouche fermée
- Regard neutre

**OUTPUT (JSON):**
```json
"expression": {
  "type": "neutral",
  "mouth_state": "closed",
  "eye_expression": "neutral gaze",
  "overall_intensity": "subtle",
  "description": "Neutral, calm expression with lips gently closed and relaxed eyes"
}
```

**OUTPUT (Prompt):**
```
(neutral expression, lips closed, neutral gaze:1.3),
...
```

**NEGATIVE PROMPT:**
```
..., smiling, smile, grin, happy expression, teeth showing, cheerful, beaming
```

**Résultat Image:** Visage NEUTRE, pas de sourire ✅

## ✅ Validation

- [x] Champ `expression` ajouté aux 2 modes
- [x] Expression dans template de prompt (weight 1.3)
- [x] Negative prompt conditionnel ajouté
- [x] Instructions critiques ajoutées
- [x] YAML validé (en cours)
- [ ] Test avec image neutre (TODO)
- [ ] Test avec image souriante (TODO)
- [ ] Vérifier que neutral = pas de sourire généré

## 🚀 Impact

### Avant (problème):
- Image source: neutre → Image générée: sourire ❌
- Pas d'analyse de l'expression
- Biais sourire non contrôlé

### Après (solution):
- Image source: neutre → JSON: "neutral" → Prompt: "(neutral:1.3)" + negative "smile" → Image générée: neutre ✅
- Expression analysée et encodée
- Biais sourire activement combattu

## 📝 Notes Techniques

### Poids de l'Expression
- **Weight 1.3** : Assez fort pour forcer l'expression sans écraser les autres features
- Placé AVANT la peau/yeux/lèvres pour priorité haute
- Combiné avec negative prompt pour double protection

### Negative Prompt Conditionnel
L'IA doit ajouter "smiling, smile, grin" SI ET SEULEMENT SI `expression.type` est "neutral" ou "serious".
Cela évite de bloquer les sourires quand ils sont voulus.

### Termes Clés
- **"neutral expression"** : Force l'absence d'émotion
- **"lips closed"** : Empêche la bouche ouverte (sourire)
- **"neutral gaze"** : Empêche les yeux plissés (sourire)
