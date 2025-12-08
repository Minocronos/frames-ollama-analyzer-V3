# Plan d'Implémentation : Mode "Lips & Skin Precision"

## 🎯 Objectif
Créer un nouveau mode d'analyse biométrique **ultra-précis** pour combler les lacunes sur :
1. **Couleur de peau** (nuances, sous-tons, variations)
2. **Lèvres** (couleur, forme détaillée, texture, asymétrie)

**Contrainte** : Ne PAS modifier les modes existants (`biometric_complete`, `deepstack_biometrics`).

---

## 🏗️ Architecture

### 1. Nouveau Mode : `biometric_lips_skin_precision`

**Emplacement** : `config/prompts.yaml`

**Description** : 
> "[1 Image] PRECISION ANALYSIS. Ultra-detailed extraction of skin color (undertones, zones) and lip morphology (color, cupid's bow, texture, asymmetry)."

---

## 📋 Schéma JSON Enrichi

### Améliorations par rapport au schéma existant :

#### A. Section `skin` (ENRICHIE)
```json
"skin": {
  "fitzpatrick": 2,
  "base_color": {
    "primary": "warm beige",
    "hex_estimate": "#D4A574",
    "undertone": "warm/cool/neutral",
    "description": "Detailed color description with regional variations"
  },
  "color_zones": {
    "forehead": "color description",
    "cheeks": "color description (blush/redness)",
    "chin": "color description",
    "under_eyes": "color description (dark circles, etc.)"
  },
  "texture": "fine/medium/coarse",
  "description": "Detailed description of pores, complexion, freckles, scars, and micro-texture"
}
```

#### B. Section `mouth` (ULTRA-DÉTAILLÉE)
```json
"mouth": {
  "lips": {
    "natural_color": {
      "upper": "natural pink with mauve undertones",
      "lower": "slightly darker rose",
      "hex_estimate_upper": "#C87E8A",
      "hex_estimate_lower": "#B86F7D",
      "description": "Detailed color description, pigmentation variations"
    },
    "shape": {
      "cupids_bow": "pronounced/subtle/flat",
      "cupids_bow_depth_mm": 3,
      "commissures": "upturned/neutral/downturned",
      "commissures_angle_deg": 5,
      "overall_shape": "full/thin/bow-shaped/heart-shaped"
    },
    "dimensions": {
      "upper_lip_mm": 10,
      "lower_lip_mm": 12,
      "ratio_upper_lower": "1:1.2",
      "width_mm": 50,
      "width_to_nose_ratio": "1:1.5"
    },
    "texture": {
      "surface": "smooth/slightly lined/dry/chapped",
      "vertical_lines": "none/subtle/pronounced",
      "description": "Detailed texture description"
    },
    "symmetry": {
      "left_right_percent": 92,
      "asymmetry_notes": "Left side slightly fuller"
    }
  },
  "philtrum": {
    "depth": "shallow/medium/deep",
    "length_mm": 15,
    "description": "Detailed philtrum description"
  },
  "mandibular_angle_deg": 115
}
```

---

## 🔧 Modifications Techniques

### Étape 1 : Ajouter le nouveau mode dans `prompts.yaml`
- [x] Créer la section `biometric_lips_skin_precision`
- [x] Définir le template avec instructions ultra-précises
- [x] Inclure le nouveau schéma JSON

### Étape 2 : Aucune modification du code Python nécessaire !
**Pourquoi ?** Le système actuel est déjà modulaire :
- `app.py` charge dynamiquement les modes depuis `prompts.yaml`
- `ResultAdapter.extract_json()` parse automatiquement tout JSON valide
- L'UI affiche automatiquement le nouveau mode dans le dropdown

### Étape 3 : Test
1. Relancer l'app
2. Sélectionner le nouveau mode `biometric_lips_skin_precision`
3. Analyser une image test
4. Vérifier que le JSON contient les nouveaux champs

---

## 📊 Comparaison des Modes

| Mode | Skin Detail | Lips Detail | Use Case |
|------|-------------|-------------|----------|
| `biometric_complete` | ⭐⭐ Basic | ⭐⭐ Basic | General biometrics + style variants |
| `deepstack_biometrics` | ⭐⭐⭐ Good | ⭐⭐ Basic | Technical report with measurements |
| `biometric_lips_skin_precision` | ⭐⭐⭐⭐⭐ Ultra | ⭐⭐⭐⭐⭐ Ultra | Makeup artists, dermatology, character design |

---

## ✅ Validation

1. Le JSON doit inclure `skin.base_color.hex_estimate`
2. Le JSON doit inclure `mouth.lips.natural_color.hex_estimate_upper`
3. Le JSON doit inclure `mouth.lips.shape.cupids_bow`
4. Aucune régression sur les modes existants

---

## 🚀 Prochaines Étapes

1. ✅ Créer ce plan (FAIT)
2. ⏳ Implémenter le nouveau mode dans `prompts.yaml`
3. ⏳ Tester sur une image réelle
4. ⏳ Documenter dans `docs/ANALYZER_GUIDE.md`
