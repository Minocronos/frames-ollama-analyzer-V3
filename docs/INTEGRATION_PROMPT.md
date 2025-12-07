# Integration Prompt for AI Assistant

## Context
I have a Streamlit application (`frames-analyzer-V3`) with two powerful image analysis modes that I want to integrate into another interface. These modes use Ollama with vision models (like Qwen3-VL) to analyze images.

## Modes to Integrate

### 1. **Perfect Reproduction Auto** (Single Image Mode)
- **Purpose**: Analyze ONE image in 6 surgical layers (Face, Body, Fashion, Background, Color, Style) and generate a perfect reproduction prompt.
- **Input**: 1 image
- **Output**: 
  - Detailed layer-by-layer analysis
  - 1 final copy-ready prompt for image generation

### 2. **Qwen Weighted Fusion** (Multi-Image Mode)
- **Purpose**: Analyze 2+ images with weight sliders and granular focus (Character/Face, Pose/Body, Clothing, Background, Colors, Style).
- **Input**: 2+ images + user-assigned weights (0.0-2.0) + focus selection per image
- **Output**:
  - 🧠 Fusion Logic (reasoning)
  - 📸 Multi-Image Description (preserves all variations: "in the first image... in the second image...")
  - 🎯 ⭐ UNIFIED FUSION ⭐ (final prompt for image generation based on weights)

## Technical Implementation

### Configuration Files

**prompts.yaml** (located in `config/prompts.yaml`):
```yaml
# Extract these two modes:
perfect_reproduction_auto:
  description: "🖼️ SINGLE IMAGE. One-Click Perfection..."
  template: |
    [Full template here - see lines 899-952 in config/prompts.yaml]

qwen_weighted_fusion:
  description: "🎨 MULTI-IMAGE FUSION (2+ images recommended)..."
  template: |
    [Full template here - see lines 808-880 in config/prompts.yaml]
```

### Core Logic (Python)

**How it works in the current app** (`app.py`):

1. **Load prompt template** from YAML:
```python
import yaml
with open("config/prompts.yaml", "r", encoding="utf-8") as f:
    prompts = yaml.safe_load(f)

template_str = prompts["analysis_modes"][analysis_mode]["template"]
```

2. **For Weighted Fusion - Inject weight context**:
```python
if "fusion" in analysis_mode.lower():
    weights_info = []
    for idx, real_idx in enumerate(selected_indices):
        w = st.session_state.get(f"weight_{real_idx}", 1.0)
        focus = st.session_state.get(f"focus_{real_idx}", "All Image")
        
        info_parts = []
        if w != 1.0:
            info_parts.append(f"Weight {w}")
        if focus != "All Image":
            info_parts.append(f"Focus: {focus}")
        
        if info_parts:
            weights_info.append(f"- Image {idx+1}: {', '.join(info_parts)}")
    
    if weights_info:
        weight_context = "\n\n**USER ASSIGNED WEIGHTS & FOCUS:**\n" + "\n".join(weights_info) + "\n\n"
        prompt_text = weight_context + template_str
```

3. **Send to Ollama vision model**:
```python
from core.gemini_adapter import GeminiAdapter

adapter = GeminiAdapter(
    model_name="qwen3-vl:235b-instruct-cloud",
    temperature=0.7
)

# Stream response
for chunk in adapter.analyze(selected_images, prompt_text, stream=True):
    full_response += chunk
```

4. **Extract and display prompts with copy buttons**:
```python
import re

# Extract code blocks (prompts are between ``` ```)
code_blocks = re.findall(r'```(?:\w+)?\s*\n(.*?)\n\s*```', full_response, re.DOTALL)

# Look for section headers (## 🎯, ## 📸, etc.)
section_pattern = r'##\s*([🎯📸🧠🚀⚡💎🔥🔬][^#\n]+)\s*\n.*?```(?:\w+)?\s*\n(.*?)\n\s*```'
matches = re.finditer(section_pattern, full_response, re.DOTALL)

for match in matches:
    title = match.group(1).strip()
    content = match.group(2).strip()
    # Display with copy button (Streamlit uses st.code())
    st.code(content, language='text')
```

## Integration Task

I need you to help me integrate these two modes into my [NEW INTERFACE NAME/TYPE].

### Requirements:
1. **Adapt the UI** to:
   - For Perfect Reproduction: Simple 1-image upload
   - For Weighted Fusion: Multi-image upload with weight sliders (0.0-2.0) and focus dropdowns per image
   
2. **Use the exact same prompts** from `config/prompts.yaml` (lines 808-880 and 899-952)

3. **Connect to Ollama** (or equivalent vision API) to send images + prompt

4. **Parse the response** to extract:
   - Code blocks between ``` ```
   - Section titles with emojis (🎯, 📸, 🧠)
   
5. **Display results** with:
   - Visual separation between sections
   - Easy copy buttons for each prompt
   - Clear indication of which prompt is the "FINAL" one (🎯 UNIFIED FUSION for multi-image)

### Key Files to Reference:
- `config/prompts.yaml` (lines 808-880 for Weighted Fusion, 899-952 for Perfect Reproduction)
- `app.py` (lines 534-624 for the analysis logic and UI)
- `core/gemini_adapter.py` (for Ollama API integration)

### Focus Options (for Weighted Fusion):
```python
focus_options = [
    "All Image",
    "Character/Face",
    "Pose/Body",
    "Clothing",
    "Background",
    "Colors/Palette",
    "Style/Ambiance"
]
```

## Expected Behavior

### Perfect Reproduction Auto (1 image):
User uploads 1 image → Click "Analyze" → Get:
- 🔬 SURGICAL LAYER ANALYSIS (6 layers)
- 🚀 PERFECT REPRODUCTION PROMPT (copy-ready)

### Qwen Weighted Fusion (2+ images):
User uploads multiple images → Assigns weights and focus per image → Click "Analyze" → Get:
- 🧠 Fusion Logic
- 📸 MULTI-IMAGE DESCRIPTION (preserves all: "in first image... in second...")
- 🎯 ⭐ UNIFIED FUSION ⭐ ← **USE THIS FOR IMAGE GENERATION**

## Questions for You (AI Assistant):

1. Can you help me adapt these modes to work in [MY TARGET INTERFACE]?
2. How should I structure the API calls to Ollama?
3. Can you create the UI components for weight sliders and focus selectors?
4. How do I parse and display the results with proper copy buttons?

Please provide code examples and step-by-step integration instructions.
