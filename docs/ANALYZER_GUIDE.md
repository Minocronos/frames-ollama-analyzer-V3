# 📊 Guide des Modes d'Analyse

## Vue d'ensemble rapide

| Mode | Type | Nb Images | Contrôle | Longueur Sortie | Cas d'usage principal |
|------|------|-----------|----------|-----------------|----------------------|
| **Perfect Reproduction Auto** | 🖼️ Single | 1 | ❌ Aucun | Long (analyse + prompt) | Reproduction fidèle d'une image |
| **Qwen Image Prompt T2I** | 🖼️ Single | 1 | ❌ Aucun | Court (1 ligne structurée) | Format technique pour pipelines |
| **Qwen Image Fusion** | 🎨 Multi | 2 | ❌ Aucun | Court (1 prompt) | Mettre un sujet dans un univers |
| **Qwen Weighted Fusion** | 🎨 Multi | 2+ | ✅ Total | Long (3 prompts) | Fusion complexe et précise |
| **Biome Ultra Detailed** | 🖼️ Single | 1 | ❌ Aucun | Très long (JSON + 6 prompts) | Analyse biométrique complète |
| **Ultimate Biome Fashion Icon** | 🖼️ Single | 1 | ❌ Aucun | Long (JSON + 3 looks) | Mode/Fashion avec biométrie |
| **Biometric Lips & Skin Precision** ⭐ | 🖼️ Single | 1 | ❌ Aucun | Long (JSON enrichi + rapport) | Couleurs peau/lèvres ultra-précises |
| **Biometric Compact & Weighted** ⭐⚠️ | 🖼️ Single | 1 | ❌ Aucun | Court (JSON + prompt < 200 mots) | **ANTI SAME FACE SYNDROME** |
| **Fetish Mode Shorts** | 🖼️ Single | 1 | ❌ Aucun | Long (JSON + 6 prompts courts) | Érotique/Mode provocante |

---

## 🖼️ MODES SINGLE IMAGE (1 image)

### Perfect Reproduction Auto

**Description :** Analyse chirurgicale en 6 couches pour recréer une image à l'identique.

**Sortie :**
- 🔬 Analyse détaillée en 6 couches :
  - Layer 1: Face (texture peau, yeux, bouche, cheveux)
  - Layer 2: Body (pose, anatomie, tension musculaire)
  - Layer 3: Fashion (vêtements, textures, accessoires)
  - Layer 4: Background (environnement, profondeur)
  - Layer 5: Light/Color (éclairage, palette, contraste)
  - Layer 6: Style (photographie, grain, esthétique)
- 🚀 1 prompt final de reproduction

**✅ Points forts :**
- Analyse ultra-détaillée et structurée
- Parfait pour comprendre une image en profondeur
- Prompt final très complet et naturel
- Idéal pour la reproduction fidèle

**❌ Limites :**
- Sortie longue (peut être trop verbeux)
- Pas de contrôle granulaire
- Uniquement 1 image

**Quand l'utiliser :**
- Tu veux reproduire une photo à l'identique
- Tu veux comprendre ce qui rend une image efficace
- Tu as besoin d'un brief technique détaillé

---

### Qwen Image Prompt T2I

**Description :** Génère un prompt ultra-précis et structuré pour Qwen-Image.

**Sortie :**
- 1 prompt structuré en sections : `[SUBJECT] . [ENVIRONMENT] . [TECHNICAL] . [STYLE] . [TYPOGRAPHY]`

**✅ Points forts :**
- Format standardisé et prévisible
- Facile à parser par des scripts
- Compact (1 ligne)
- Optimisé pour Qwen-Image (20B MMDiT)

**❌ Limites :**
- Moins narratif que Perfect Reproduction
- Format rigide
- Uniquement 1 image

**Quand l'utiliser :**
- Tu utilises Qwen-Image spécifiquement
- Tu veux un format standardisé pour l'automatisation
- Tu as besoin d'un prompt court et structuré

---

### Biome Ultra Detailed

**Description :** Analyse biométrique complète + prompts hybrides (narratif + métriques).

**Sortie :**
- 📋 JSON biométrique avec mesures précises (angles, mm, ratios)
- 🎨 3 Visual Interpretations (Natural, Fashion, Cinematic) - longs et détaillés
- ⚡ 3 Detailed Prompts (versions condensées avec métriques)

**✅ Points forts :**
- JSON ultra-détaillé avec métriques techniques
- Prompts hybrides (mélange artistique + chiffres)
- 6 prompts au total (variations multiples)
- Downloadable JSON avec timestamp

**❌ Limites :**
- Sortie très longue
- Peut être overkill pour un usage simple
- Uniquement 1 image

**Quand l'utiliser :**
- Tu veux des données biométriques précises
- Tu as besoin de plusieurs variations de prompts
- Tu veux mélanger créativité et précision technique

---

### Ultimate Biome Fashion Icon

**Description :** JSON biométrique + 3 looks mode (Intimate Couture, Avant-Garde, Raw Editorial).

**Sortie :**
- 📋 JSON biométrique
- 💎 3 prompts mode distincts avec des vibes différentes

**✅ Points forts :**
- Focus mode/fashion
- 3 variations stylistiques automatiques
- Inspire du Helmut Newton, Met Gala, Peter Lindbergh

**❌ Limites :**
- Spécialisé mode haute couture
- Pas adapté pour d'autres types d'images
- Uniquement 1 image

**Quand l'utiliser :**
- Tu travailles dans la mode
- Tu veux des variations éditoriales sophistiquées
- Tu as besoin de références biométriques + créatives

---

### Biometric Lips & Skin Precision ⭐ NEW

**Description :** Analyse biométrique ULTRA-PRÉCISE focalisée sur la couleur de peau et la morphologie des lèvres.

**Sortie :**
- 📋 JSON biométrique enrichi avec :
  - **Skin** : Couleur hex, sous-tons (warm/cool/neutral), zones faciales (front, joues, menton, sous-yeux)
  - **Lips** : Couleur hex (lèvre sup/inf), arc de Cupidon (profondeur, forme), commissures, texture, asymétrie, philtrum
- 📊 Rapport technique détaillé avec mesures précises
- 🎨 Fragments de prompts optimisés (skin + lips)

**✅ Points forts :**
- **Précision extrême** sur peau et lèvres (hex colors, sous-tons, zones)
- Détection maquillage vs couleur naturelle
- Analyse arc de Cupidon, commissures, philtrum
- Parfait pour makeup artists, dermatologie, character design
- Compatible avec le système de verrouillage d'identité

**❌ Limites :**
- Spécialisé (focus sur 2 aspects uniquement)
- Sortie technique (moins créative que les modes fashion)
- Uniquement 1 image

**Quand l'utiliser :**
- Tu as besoin de couleurs de peau/lèvres **exactes** (hex codes)
- Tu travailles en makeup, cosmétiques, dermatologie
- Les modes biométriques classiques manquent de précision sur ces aspects
- Tu veux verrouiller une identité avec couleurs ultra-précises

---

### Biometric Compact & Weighted ⭐ NEW - ANTI SAME FACE

**Description :** Prompts ultra-courts (< 200 mots) avec poids visuels (1.1-1.5) pour Stable Diffusion/Flux. **Résout le "same face syndrome"**.

**Sortie :**
- 📋 JSON biométrique (référence)
- 🎯 **COMPACT WEIGHTED PROMPT** (< 200 mots avec poids)
  - Format: `(feature:1.5)` pour features très distinctives
  - Ordre stratégique: features uniques en premier
- ❌ **NEGATIVE PROMPT** (critique pour la diversité)
- 📊 **WEIGHT EXPLANATION** (rationale des poids)
- 🔄 **FORMATS ALTERNATIFS** (natural language, keyword list)

**Système de Poids :**
- **1.5** : TRÈS distinctif (asymétries, features rares)
- **1.4** : Hautement distinctif (proportions inhabituelles, marques)
- **1.3** : Distinctif (couleurs rares, formes uniques)
- **1.2** : Notable (sous-tons spécifiques, texture)
- **1.1** : Standard mais important (âge, structure de base)

**✅ Points forts :**
- **RÉSOUT LE SAME FACE SYNDROME** (problème #1 des générateurs)
- Prompts ultra-courts = meilleure attention du modèle
- Poids visuels forcent les features uniques
- Negative prompts inclus automatiquement
- Focus sur asymétries et traits distinctifs
- Compatible Stable Diffusion, Flux, ComfyUI
- Formats alternatifs pour tous les modèles

**❌ Limites :**
- Nécessite un modèle supportant les poids (ou utiliser format alternatif)
- Moins de détails techniques que les modes longs
- Uniquement 1 image

**Quand l'utiliser :**
- ⚠️ **TU AS LE PROBLÈME "TOUJOURS LE MÊME VISAGE"** ← USE THIS!
- Tu génères avec Stable Diffusion, Flux, ComfyUI
- Tu veux des visages vraiment distincts et mémorables
- Les prompts longs ne donnent pas de bons résultats
- Tu as besoin de negative prompts optimisés

### Fetish Mode Shorts

**Description :** 6 prompts érotiques/fetish courts et intenses (Latex, Bondage, Leather, Wet, Dominatrix, Underboob).

**Sortie :**
- 📋 JSON biométrique simplifié
- 🔥 6 prompts courts (80-100 mots chacun)

**✅ Points forts :**
- 6 variations thématiques automatiques
- Style éditorial (Helmut Newton, Ellen von Unwerth)
- Prompts courts et directs
- Force l'inclusion du genre (évite les erreurs)

**❌ Limites :**
- Contenu adulte/spécialisé
- Pas adapté pour tout type de projet
- Uniquement 1 image

**Quand l'utiliser :**
- Tu génères des images érotiques/mode provocante
- Tu veux plusieurs variations thématiques
- Tu as besoin d'un style éditorial haute couture

---

## 🎨 MODES MULTI-IMAGE (2+ images)

### Qwen Image Fusion (2 images)

**Description :** Fusion automatique simple : Image 1 = Sujet, Image 2 = Style/Environnement.

**Sortie :**
- 1 prompt fusionné

**✅ Points forts :**
- Simple et rapide (aucun réglage)
- Logique claire et prévisible
- Parfait pour "mettre X dans l'univers de Y"

**❌ Limites :**
- Logique fixe (pas de flexibilité)
- Exactement 2 images (pas 3+)
- Pas de contrôle granulaire

**Quand l'utiliser :**
- Tu veux placer un personnage dans un nouvel environnement
- Tu as exactement 2 images
- Tu veux un résultat rapide sans réglages

---

### Qwen Weighted Fusion (2+ images) ⭐

**Description :** Fusion avancée avec sliders de poids (0.0-2.0) et focus granulaire par image.

**Sortie :**
- 🧠 Fusion Logic (raisonnement avec poids/focus)
- 📸 Multi-Image Description (préserve toutes les variations)
- 🎯 ⭐ UNIFIED FUSION ⭐ (prompt final pour génération) ← **Utilise celui-ci !**

**Focus disponibles :**
- All Image
- Character/Face
- Pose/Body
- Clothing
- Background
- Colors/Palette
- Style/Ambiance

**✅ Points forts :**
- Contrôle chirurgical total
- Supporte 2, 3, 4+ images
- 3 sorties (analyse + variations)
- Parfait pour les fusions complexes

**❌ Limites :**
- Demande plus de configuration (poids + focus)
- Peut être complexe pour un usage simple
- Sortie longue

**Quand l'utiliser :**
- Tu veux un contrôle précis sur ce qui est extrait de chaque image
- Tu mixes 3+ images
- Tu as besoin de voir la logique de fusion (debug)

---

## 🎯 Arbre de décision

```
Tu as combien d'images ?
│
├─ 1 image
│  │
│  ├─ Tu veux reproduire fidèlement ?
│  │  └─ → Perfect Reproduction Auto
│  │
│  ├─ Tu veux un format technique/structuré ?
│  │  └─ → Qwen Image Prompt T2I
│  │
│  ├─ Tu veux des données biométriques + créatif ?
│  │  └─ → Biome Ultra Detailed
│  │
│  ├─ Tu travailles dans la mode ?
│  │  └─ → Ultimate Biome Fashion Icon
│  │
│  └─ Tu veux du contenu érotique/fetish ?
│     └─ → Fetish Mode Shorts
│
└─ 2+ images
   │
   ├─ Tu veux juste "Sujet + Style" (simple) ?
   │  └─ → Qwen Image Fusion (2 images exactement)
   │
   └─ Tu veux un contrôle total (avancé) ?
      └─ → Qwen Weighted Fusion (2+ images)
```

---

## 💡 Conseils pratiques

### Pour la reproduction d'images
1. **Perfect Reproduction Auto** (meilleur choix général)
2. **Qwen Image Prompt T2I** (si tu veux du structuré)

### Pour la fusion d'images
1. **Qwen Weighted Fusion** (si tu veux du contrôle)
2. **Qwen Image Fusion** (si tu veux du rapide)

### Pour la biométrie + créatif
1. **Biome Ultra Detailed** (le plus complet)
2. **Ultimate Biome Fashion Icon** (spécialisé mode)

### Pour des démos
- **Qwen Image Fusion** : Simple, facile à expliquer
- **Perfect Reproduction Auto** : Impressionnant, détaillé

---

## 🔥 Comparaison : Perfect Reproduction vs T2I

| Critère | Perfect Reproduction Auto | Qwen Image Prompt T2I |
|---------|--------------------------|----------------------|
| **Format** | Narratif fluide | Structuré (sections) |
| **Longueur** | Long (analyse + prompt) | Court (1 ligne) |
| **Lisibilité** | Naturel, storytelling | Technique, parsable |
| **Usage** | Reproduction manuelle | Automatisation/API |
| **Détails** | Très riche | Précis mais compact |

**Verdict :** Perfect Reproduction pour l'humain, T2I pour les machines.

---

## 🎨 Comparaison : Image Fusion vs Weighted Fusion

| Critère | Qwen Image Fusion | Qwen Weighted Fusion |
|---------|------------------|---------------------|
| **Complexité** | Simple (0 réglages) | Avancée (sliders + focus) |
| **Images** | Exactement 2 | 2, 3, 4+ |
| **Logique** | Fixe (Img1=Sujet, Img2=Style) | Personnalisée |
| **Sorties** | 1 prompt | 3 prompts |
| **Contrôle** | ❌ Aucun | ✅ Total |

**Verdict :** Fusion pour la démo, Weighted Fusion pour la précision.

---

## 📚 Ressources

- **Integration Prompt** : `docs/INTEGRATION_PROMPT.md` (pour intégrer ces modes ailleurs)
- **Config Prompts** : `config/prompts.yaml` (templates de tous les modes)
- **PRD** : `docs/PRD.md` (Product Requirements)
