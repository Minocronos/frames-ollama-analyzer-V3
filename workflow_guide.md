# 🧠 Gemini 3 Analysis Workflow Guide

This guide explains how the AI "thinks" based on your inputs and the chosen **Analysis Mode**. Use this to master the tool.

## 1. The Input Logic (What you feed it)

| Input Type | Best For | How Gemini Perceives It |
| :--- | :--- | :--- |
| **Single Image/Frame** | Detailed Analysis, T2I Prompts | A static canvas. It extracts maximum detail from every pixel. |
| **Multi-Frame (Sequence)** | Video Analysis, Motion Tracking | A flow of time. It looks for changes, movement, and narrative progression. |
| **Multi-Image (Mix)** | Concept Fusion, Style Transfer | A palette of ideas. It looks for relationships or combines elements (e.g., Subject A + Style B). |

---

## 2. The Analysis Modes (How it processes)

### 📐 Mode: DeepStack Biometrics
*Goal: Scientific & Anatomical Precision.*
- **Output**: A rigorous report with estimated measurements (mm, degrees, %), morphology, and spatial coordinates.
- **Use Case**: Character consistency, 3D modeling reference, medical/fitness analysis.

### 📸 Mode: Qwen Image Prompt T2I
*Goal: The Ultimate "Digital Twin" Prompt.*
- **Logic**: It deconstructs the image into 5 layers: **Subject (Biometrics)**, **Pose**, **Attire**, **Environment**, and **Technical Specs**.
- **Output**: A strictly formatted prompt optimized for Qwen-Image (20B) and other high-fidelity T2I models.
- **Key Feature**: Includes precise percentages ("Occupies 40% of frame") and directional instructions ("Body turned 30° right").

### 🧬 Mode: Qwen Image Fusion
*Goal: Conceptual Alchemy.*
- **Input Requirement**: Select **2+ Images**.
- **Logic**:
    - **Image 1**: Extracts the **SUBJECT** (Identity, Pose, Body).
    - **Image 2**: Extracts the **STYLE & ENVIRONMENT** (Lighting, Vibe, Art Direction).
- **Output**: A single prompt that places Subject A into World B.

### ⚖️ Mode: Qwen Weighted Fusion
*Goal: Precision-Controlled Fusion with Weight Sliders.*
- **Input Requirement**: Select **2+ Images** and enable **"Show Advanced Weights"** in the sidebar.
- **Logic**:
    - **High Weight (>1.0)**: This image is DOMINANT. Its subject, composition, and style take precedence.
    - **Low Weight (<1.0)**: This image is SUBTLE. Only minor details (textures, accents) are used.
    - **Neutral Weight (1.0)**: Balanced contribution (e.g., a specific prop or color).
- **Output**: 
    - **🧠 Fusion Logic**: Explains how each image was used based on its weight.
    - **🚀 Final Prompt**: A clean, highly detailed, copy-paste ready prompt (100+ words).
- **Use Case**: When you want surgical control over which image contributes what to the final result.

### 🛠️ Mode: Technical Analysis
*Goal: Cinematography & Photography breakdown.*
- **Output**: Lighting diagrams, camera lens choices, composition rules (Rule of Thirds), and color grading info.

### 🎨 Mode: Creative Conversion
*Goal: Artistic Re-imagining.*
- **Logic**: Takes the *content* of your image and rewrites it in a completely different style (e.g., Cyberpunk, Wes Anderson).

### 🎬 Mode: Video Prompt
*Goal: Text-to-Video Generation.*
- **Output**: Prompts optimized for Sora, Wan 2.2, Runway Gen-3. Focuses on *movement* descriptions ("Slow dolly in", "Rack focus").

---

## 3. Pro Tips for Best Results

> [!TIP]
> **For Perfect Character Consistency**:
> Use **Qwen Image Prompt T2I** on your reference image. Copy the "SUBJECT" part of the output and use it as a constant in all your future generations.

> [!TIP]
> **The "Fusion" Hack**:
> Want to see your character in a specific movie scene?
> 1. Upload your character (Image 1).
> 2. Upload a screenshot of the movie scene (Image 2).
> 3. Select both -> **Qwen Image Fusion**.
> 4. Generate!

> [!TIP]
> **Biometric Accuracy**:
> For the best **DeepStack Biometrics** results, ensure the subject is facing forward or in a 3/4 view. Extreme angles might skew the metric estimations.

> [!TIP]
> **Mastering Weight Sliders**:
> Enable **"Show Advanced Weights"** in the sidebar to unlock surgical control over fusion.
> - Set your main subject image to **1.5-2.0** (Dominant).
> - Set style/texture references to **0.3-0.7** (Subtle hints).
> - Set props or specific elements to **1.0** (Balanced integration).
> Example: Portrait (1.8) + Cyberpunk City (0.5) + Red Jacket (1.0) = Portrait wearing a red jacket with subtle neon reflections.
