# Fix Plan: Fitzpatrick Type 5 Generates Too Light Skin

## 🔴 Problem
User reports: "Fitzpatrick à 5 me fait un résultat trop clair"

**Root Cause:**
- AI models don't understand Fitzpatrick scale numbers
- "fitzpatrick: 5" is too abstract (medical term)
- Models have bias toward lighter skin (dataset issue)
- No visual description forces AI to guess

## ✅ Solution

### 1. Add Visual Description Fields
```json
"skin": {
  "fitzpatrick": 5,
  "skin_tone_visual": "deep brown skin, rich melanin, dark complexion",
  "color_hex": "#8D5524",
  "undertone": "warm/cool/neutral",
  "description": "..."
}
```

### 2. Fitzpatrick Reference Table (for AI instruction)
```
Type 1: Very pale, porcelain, ivory (#FFF5E1)
Type 2: Fair, light beige (#F5D5C5)
Type 3: Light to medium, beige (#E8C4A8)
Type 4: Olive, tan, medium brown (#C68642)
Type 5: Brown, deep brown, rich melanin (#8D5524)
Type 6: Very dark brown, deep ebony (#4A3728)
```

### 3. Prompt Strategy
**DON'T USE:**
```
Fitzpatrick type 5 skin  ← AI doesn't understand
```

**USE INSTEAD:**
```
(deep brown skin, hex #8D5524, warm undertones:1.2)
```

## 🔧 Implementation

### Files to Modify:
1. `config/prompts.yaml` - All biometric modes
2. Add `skin_tone_visual` field (MANDATORY)
3. Add Fitzpatrick reference table in instructions
4. Force AI to use visual descriptions in final prompts

### Changes:
- [x] Add `skin_tone_visual` field to all JSON schemas
- [x] Add hex color examples for each Fitzpatrick type
- [x] Update prompt templates to use visual description
- [x] Add validation: If Fitzpatrick ≥ 4, MUST use "brown/dark" terms
