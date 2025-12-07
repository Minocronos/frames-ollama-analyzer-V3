# 🎨 Artidicia - The Artificial Serendipity Engine

![Artidicia Logo](assets/logo_simple.png)

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

**AI-Powered Visual Analysis | Quantum Haute Couture Engine | Where AI Hallucination Becomes Art**

> *"Where others see errors, we see inspiration."*  
> *"Hallucination as a feature, not a bug."*

Artidicia is not just another video analysis tool—it's a **creative co-pilot** that embraces AI hallucination as a feature. Built on Ollama with support for multiple AI models, it transforms visual analysis into a journey of artificial serendipity.

---

## ✨ Core Philosophy

Traditional tools treat AI hallucination as an error to eliminate. **Artidicia celebrates it as creative fuel.**

- **Artificial Serendipity**: Let the AI's artistic interpretations guide you to unexpected places
- **Hallucination as Feature**: The AI's "mistakes" become your inspiration
- **Quantum Haute Couture**: Fuse impossible textures and materials with mathematical precision (e.g., "striped sweater in lace fabric")
- **Multi-Model Freedom**: Switch between local and cloud models seamlessly

---

## 🚀 Quick Start

```bash
run.bat
```

That's it! The app will launch on `http://localhost:8502`

---

## 🎯 Key Features

### 🎨 **Style Transfer Pro**
Transform any image while preserving the subject but radically changing the aesthetic.
- **60+ Styles** across 8 categories (Photography, Cinematic, Art Movements, Digital 3D, Fashion, etc.)
- **Anchor & Transform Logic**: Keeps pose and subject, reimagines atmosphere

### 🧠 **RLHF Dataset Builder**
Build your own training dataset with human feedback.
- **Local History**: All analyses saved in SQLite (`history.db`)
- **Star Rating System**: Rate prompts 1-5 ⭐ with comments
- **Curated Export**: Save only the best for future fine-tuning

### ⚡ **Flexible AI Backend**
- **Ollama Integration**: Use any local model (Llama, Mistral, Qwen, etc.)
- **Cloud Models**: Access Gemini, GPT, Claude via Ollama
- **Dependency Injection**: Swap AI providers without changing code

---

## 🛠️ Analysis Modes

| Mode                        | Description                                                                          |
| --------------------------- | ------------------------------------------------------------------------------------ |
| **📸 Style Transfer Pro**    | Artistic reinterpretation with 60+ styles (Wes Anderson, Cyberpunk, Kodak Portra...) |
| **💡 Studio Lighting Setup** | Reverse engineering of lighting and composition                                      |
| **🧬 Biometric Analysis**    | Precise biometric data extraction in JSON format                                     |
| **👗 Fashion Icon**          | High-fashion analysis with focus on textures and design                              |
| **👁️ Alt POV**               | Extreme camera angles and alternative aesthetics                                     |

---

## 📦 Installation & Transport

### Fresh Install
```bash
scripts\setup.bat    # Install dependencies
run.bat              # Launch the app
```

### Move to Another Machine
```bash
scripts\export.bat   # Create portable ZIP
# → Copy ZIP to new machine
# → Unzip
# → scripts\setup.bat
# → run.bat
```

---

## 📁 Project Structure

```
artidicia/
├── run.bat                  ← Main launcher
├── app.py                   ← Streamlit application
├── history.db               ← SQLite database (auto-created)
├── config/              
│   ├── prompts.yaml         ← Prompt templates (The Brain)
│   └── settings.yaml        ← Global configuration
├── core/                
│   ├── interfaces.py        ← [NEW] DI contracts
│   ├── prompt_manager.py    ← [NEW] Prompt loading
│   ├── ollama_adapter.py    ← AI model adapter
│   ├── database.py          ← SQLite manager
│   ├── result_adapter.py    ← Result formatter
│   └── video_processor.py   ← Frame extraction
├── docs/                    ← Documentation
│   └── tutorials/           ← DI learning resources
└── test_evolution.py        ← DI architecture proof
```

---

## 🏗️ Architecture Highlights

**Dependency Injection Ready**: Artidicia uses a modular architecture that makes it trivial to:
- Switch AI providers (Ollama → OpenAI → Claude)
- Change prompt sources (YAML → Database → API)
- Add image generation (ComfyUI, DALL-E, Midjourney)

See `implementation_plan.md` and `walkthrough_refactoring.md` for details.

---

## 📚 Documentation

- **[docs/CREATIVE_PHILOSOPHY.md](docs/CREATIVE_PHILOSOPHY.md)** - Why hallucination is a feature
- **[docs/INDEX.md](docs/INDEX.md)** - Complete navigation
- **[implementation_plan.md](implementation_plan.md)** - DI architecture plan
- **[walkthrough_refactoring.md](walkthrough_refactoring.md)** - Refactoring summary

---

## 🎨 Philosophy in Action

Artidicia doesn't just analyze—it **co-creates**. The AI's unexpected interpretations, artistic drift, and serendipitous connections aren't bugs to fix. They're features to celebrate.

**Welcome to artificial serendipity.** 🚀
