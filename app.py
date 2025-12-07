import streamlit as st
import yaml
import os
import json
from pathlib import Path
from core.video_processor import VideoProcessor
from core.ollama_adapter import OllamaAdapter
from core.database import DatabaseManager
# from ui.components import render_flow_graph  # Temporarily disabled
from jinja2 import Template
import ollama

# Initialize Database
db = DatabaseManager()

# Page Config (Must be first)
st.set_page_config(
    page_title="Artidicia - Artificial Serendipity",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Config with Cache
from core.prompt_manager import YamlPromptLoader

# Initial Load using Dependency Injection
# In a real DI framework, this would be injected, but here we wire it up manually at the start.
loader = YamlPromptLoader()

@st.cache_data
def load_config():
    return loader.load_config()

settings, prompts = load_config()

# Sidebar Reload Button (Must be placed early to affect the rest of the script)
with st.sidebar:
    if st.button("🔄 Reload Config"):
        load_config.clear()
        st.rerun()

# Custom CSS for "Bold & Premium" Look
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #161B22;
        border-right: 1px solid #30363D;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    h1 {
        background: linear-gradient(90deg, #FF4B4B 0%, #FF914D 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(90deg, #FF4B4B 0%, #FF914D 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        opacity: 0.9;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(255, 75, 75, 0.3);
    }
    
    /* Cards/Containers */
    .css-1r6slb0 {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 12px;
        padding: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("🎨 Artidicia 👁️")
    st.caption("🚀 The Engine for **Quantum Haute Couture**")
    st.caption("*Fusion Logic & Biometric Fidelity*")
    
    # Model Selection
    try:
        models_info = ollama.list()
        
        model_names = []
        if hasattr(models_info, 'models'):
            for m in models_info.models:
                if hasattr(m, 'model'):
                    model_names.append(m.model)
                elif isinstance(m, dict) and 'name' in m:
                    model_names.append(m['name'])
                elif isinstance(m, dict) and 'model' in m:
                    model_names.append(m['model'])
                else:
                    model_names.append(str(m))
        else:
            for m in models_info:
                 if isinstance(m, dict):
                    model_names.append(m.get('name', m.get('model', 'unknown')))
                 else:
                    model_names.append(str(m))

        default_model = settings['model']['name']
        if default_model not in model_names:
            model_names.insert(0, default_model)
            
        selected_model = st.selectbox(
            "Select Model",
            options=model_names,
            index=model_names.index(default_model) if default_model in model_names else 0
        )
    except Exception as e:
        st.error(f"Could not fetch models: {e}")
        selected_model = settings['model']['name']
        st.caption("Using default from settings due to error.")

    st.caption(f"Active: `{selected_model}`")
    
    st.header("Input Source")
    input_mode = st.radio(
        "Select Input Type",
        options=["Video Only", "Images Only", "Video + Images (Mix)"],
        index=1,
        help="Choose whether to analyze video frames, uploaded images, or both combined."
    )
    
    st.header("Configuration")
    def format_mode_name(mode_key):
        desc = prompts["analysis_modes"][mode_key].get("description", "")
        name = mode_key.replace("_", " ").title()
        
        # Add icons based on tags
        if "[1 Image]" in desc:
            return f"📸 {name}"
        elif "[2 Images]" in desc:
            return f"👥 {name}"
        elif "[Multi-Image]" in desc:
            return f"🎨 {name}"
        else:
            return f"⚙️ {name}"

    # Determine default index for qwen_weighted_fusion
    mode_options = list(prompts["analysis_modes"].keys())
    default_mode_index = 0
    if "alt_pov" in mode_options:
        default_mode_index = mode_options.index("alt_pov")
    elif "qwen_weighted_fusion" in mode_options:
        default_mode_index = mode_options.index("qwen_weighted_fusion")

    analysis_mode = st.selectbox(
        "Analysis Mode",
        options=mode_options,
        index=default_mode_index,
        format_func=format_mode_name,
        help="Choose how the AI should analyze the frames."
    )
    
    # Show description of selected mode
    mode_description = prompts["analysis_modes"][analysis_mode].get("description", "")
    if mode_description:
        with st.expander("ℹ️ Mode Description", expanded=False):
            st.markdown(mode_description)
    
    if analysis_mode == "style_transfer_pro":
        # Two-step style selection
        style_category = st.selectbox(
            "Style Category",
            options=list(prompts["style_categories"].keys()),
            help="Choose a category first"
        )
        
        selected_style = st.selectbox(
            "Specific Style",
            options=prompts["style_categories"][style_category],
            help="Choose the exact style to apply"
        )
    elif analysis_mode == "alt_pov":
        selected_style = None
        # ALT POV Look Selector
        alt_pov_looks = [
            "1. Latex Noir (Low Angle)", "2. Leather Darkness (Overhead)", "3. Industrial Abyss (Worm's Eye)", 
            "4. X-Ray (Medical)", "5. Security Glitch (CCTV)", "6. Mirror Maze (Reflections)", 
            "7. Submerged (Underwater)", "8. Inverted Gravity (Upside Down)", "9. Thermal Vision (Heatmap)", 
            "10. Micro Neon (Macro)", "11. Anamorphic Bokeh (Cinematic)", "12. Reflection Fracture (Broken Mirror)", 
            "13. Drone Aerial (High Angle)", "14. Tilt-Shift (Miniature)", "15. PVC Chrome (Fisheye)", 
            "16. Soft Focus (Dreamy)", "17. Ethereal Veil (Through Fabric)", "18. Golden Hour (Backlit)", 
            "19. Thigh-High Chaos (Extreme Low)", "20. Shibari Suspension (Inverted)", "21. Lingerie Riot (Intimate)", 
            "22. Booty Shorts (Rear View)", "23. Latex Noir Chrome (Throne)", "24. Sheer Bondage (Overhead)", 
            "25. Leather & Lace (Over-Shoulder)", "26. Wet Look (Poolside)", "27. Dominatrix Edge (Power Stance)", 
            "28. Underboob Tease (Golden Hour Low)"
        ]
        
        selected_looks = st.multiselect(
            "Select Looks to Generate",
            options=alt_pov_looks,
            default=["21. Lingerie Riot (Intimate)"], # Default to avoid accidental 28-look generation
            help="Choose specific looks. If you uncheck all, it might generate ALL 28 (Warning!)"
        )
        
        # Store selection in session state to use during analysis
        st.session_state['alt_pov_selection'] = selected_looks
        
        
        # Look Fidelity Slider
        st.divider()
        look_fidelity = st.slider(
            "🎚️ Fidélité (0-45% Source | 46-75% Mix | 76%+ Look)",
            min_value=0,
            max_value=100,
            value=70,
            step=5,
            help="0-45%: Garde Tenue Source | 46-75%: Mélange | 76-100%: Remplace par le Look",
            format="%d%%"
        )
        st.session_state['look_fidelity'] = look_fidelity
        st.caption("📏 **Zones:** 0-45% (Keep Source Outfit) | 46-75% (Mix) | 76-100% (Replace with Look)")
        
        # Visual feedback
        if look_fidelity <= 30:
            st.caption("🎨 **Mode: Source Dominant** - LOOK provides aesthetic inspiration, keeps your clothing/pose")
        elif look_fidelity <= 60:
            st.caption("⚖️ **Mode: Balanced Blend** - Mix of LOOK style and source material")
        elif look_fidelity <= 85:
            st.caption("🔥 **Mode: LOOK Dominant** - Strong LOOK application, adapted to your subject")
        else:
            st.caption("⚡ **Mode: Pure LOOK** - Strict LOOK definition, source = biometrics only")
            
        with st.expander("💡 STRATEGY GUIDE: Focus vs Fidelity"):
            st.markdown("""
            **La Règle d'Or pour éviter les conflits :**
            
            1. **Je veux GARDER ma tenue d'origine (Fidelity 0-40%)**
               👉 Mettez le Focus Image sur **"All Image"**.
               *(Si vous mettez "Face only", l'IA ne verra pas la tenue à garder !)*
               
            2. **Je veux CHANGER de look (Fidelity 60-100%)**
               👉 Mettez le Focus Image sur **"Character/Face"**.
               *(Cela évite que votre vieux t-shirt ne "bave" sur le nouveau costume)*

            ---
            **⚡ Astuce FUSION (2 Images) :**
            *   **Image A (Visage)** : Focus **"Face"** (Poids 1.5 - 1.8) -> *Verrouille l'identité + Coiffure.*
            *   **Image B (Pose)** : Focus **"Pose"** (Poids 1.2) -> *Extrait le squelette (Ignore vêtements).*
            *(⚠️ Pour garder aussi la tenue de l'image B, mettez son Focus sur "All Image" !)*
            """)
        
    else:
        selected_style = None

    st.divider()
    show_weights = st.checkbox("Show Advanced Weights ⚖️", value=True, key="show_weights", help="Enable weight sliders for image fusion.")
        

    
    st.divider()
    st.divider()
    
    # Temperature Slider (Moved to bottom)
    with st.expander("🌡️ Advanced: Creativity (Temperature)", expanded=False):
        col_temp, col_reset = st.columns([3, 1])
        with col_reset:
            st.write("") # Spacer
            if st.button("↺", help="Reset to Default (0.7)"):
                st.session_state['temp_value'] = 0.7
                
        with col_temp:
            temperature = st.slider(
                "Value",
                min_value=0.0,
                max_value=5.0,
                value=st.session_state.get('temp_value', settings['model']['temperature']),
                step=0.1,
                key='temp_value',
                help="0.0 = Precise, 1.0 = Creative, >2.0 = TOTAL CHAOS"
            )

    st.info("Hot-Reload Active: Edit `prompts.yaml` to see changes instantly.")

# Main Content
st.title("Video Intelligence & Art")
st.markdown("Upload a video to explore **artificial serendipity**. *Hallucination as a feature, not a bug.*")

# File Upload (conditional based on input mode)
uploaded_file = None
uploaded_images = None

if input_mode == "Video Only":
    uploaded_file = st.file_uploader("📹 Drop your video here", type=['mp4', 'mov', 'avi'])
elif input_mode == "Images Only":
    uploaded_images = st.file_uploader(
        "📷 Upload your images here",
        type=["jpg", "jpeg", "png", "webp"],
        accept_multiple_files=True
    )
    if uploaded_images:
        st.success(f"✅ {len(uploaded_images)} image(s) uploaded")
else:  # Video + Images (Mix)
    col_v, col_i = st.columns(2)
    with col_v:
        uploaded_file = st.file_uploader("📹 Video", type=['mp4', 'mov', 'avi'])
    with col_i:
        uploaded_images = st.file_uploader(
            "📷 Images",
            type=["jpg", "jpeg", "png", "webp"],
            accept_multiple_files=True
        )
        if uploaded_images:
            st.caption(f"✅ {len(uploaded_images)} image(s)")

# Handle Images Only mode
if uploaded_images and not uploaded_file:
    from PIL import Image
    
    # Load images
    all_frames = []
    for img_file in uploaded_images:
        img = Image.open(img_file)
        all_frames.append(img)
    
    # Store in session state
    # Detect if new images were uploaded by comparing names
    current_names = [img_file.name for img_file in uploaded_images]
    previous_names = st.session_state.get('image_names', [])
    
    if current_names != previous_names:
        # New upload detected
        previous_count = len(previous_names)
        current_count = len(current_names)
        
        st.session_state['uploaded_images_list'] = all_frames
        st.session_state['image_names'] = current_names
        
        # ALSO populate cached_images for the unified analysis section
        st.session_state['cached_images'] = all_frames
        st.session_state['cached_img_names'] = current_names
        
        # Smart selection: only select NEW images, preserve existing selections
        if current_count > previous_count:
            # New images added - select only the new ones
            for i in range(previous_count, current_count):
                st.session_state[f"frame_select_{i}"] = True
        else:
            # Complete replacement - select all
            for i in range(current_count):
                if f"frame_select_{i}" not in st.session_state:
                    st.session_state[f"frame_select_{i}"] = True
    
    # Display images with selection controls
    st.subheader(f"📷 {len(st.session_state['uploaded_images_list'])} Image(s) Uploaded")
    cols = st.columns(4)
    
    for i, img in enumerate(st.session_state['uploaded_images_list']):
        with cols[i % 4]:
            st.image(img, width="stretch")
            
            # Checkbox for selection (for analysis)
            st.checkbox(
                "Select for analysis",
                key=f"frame_select_{i}"
            )
            
            if show_weights:
                st.slider(
                    "Weight",
                    min_value=0.0,
                    max_value=2.0,
                    value=st.session_state.get(f"weight_{i}", 1.0),
                    step=0.1,
                    key=f"weight_{i}",
                    label_visibility="collapsed"
                )
                st.caption(f"Weight: {st.session_state.get(f'weight_{i}', 1.0)}")
                
                # Granular Focus Selector
                focus_options = [
                    "All Image",
                    "Character/Face",
                    "Pose/Body",
                    "Clothing",
                    "Background",
                    "Colors/Palette",
                    "Style/Ambiance"
                ]
                st.selectbox(
                    "Focus on:",
                    options=focus_options,
                    index=0,
                    key=f"focus_{i}",
                    label_visibility="collapsed"
                )
                st.caption(f"Focus: {st.session_state.get(f'focus_{i}', 'All Image')}")
            
            # Show filename
            st.caption(st.session_state['image_names'][i])
    
        # Removed direct analysis result display

elif uploaded_file:
    # Video preview (smaller size)
    col_preview, col_spacer = st.columns([1, 1])
    with col_preview:
        st.video(uploaded_file)
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Frame Extraction")
        
        # Extraction Settings
        extract_strategy = st.radio(
            "Extraction Method",
            ["By Interval (Seconds)", "By Count (Total Frames)"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        if extract_strategy == "By Interval (Seconds)":
            interval = st.slider("Interval (seconds)", 1, 10, 2)
            max_frames = None
        else:
            max_frames = st.slider("Number of Frames", 1, 20, 5)
            interval = None
        
        if st.button("Extract Frames", type="primary"):
            with st.spinner("Extracting frames..."):
                processor = VideoProcessor()
                
                # Extract frames using process_video
                strategy_type = "interval" if extract_strategy == "By Interval (Seconds)" else "count"
                value_param = interval if extract_strategy == "By Interval (Seconds)" else max_frames
                
                frames = processor.process_video(
                    uploaded_file,
                    strategy=strategy_type,
                    value=value_param
                )
                
                # Clear all previous selections
                keys_to_delete = [key for key in st.session_state.keys() if key.startswith('frame_select_')]
                for key in keys_to_delete:
                    del st.session_state[key]
                
                # Store ONLY video frames (not images yet)
                st.session_state['video_frames'] = frames
                st.session_state['frames_just_extracted'] = True
                
                st.success(f"✅ Extracted {len(frames)} frame(s) from video")
                st.rerun()
    
    with col2:
        # Dynamically merge video frames + uploaded images
        has_video = 'video_frames' in st.session_state and st.session_state['video_frames']
        has_images = uploaded_images is not None and len(uploaded_images) > 0
        
        if has_video or has_images:
            # Start with video frames
            all_items = []
            item_labels = []
            
            if has_video:
                for i, frame in enumerate(st.session_state['video_frames']):
                    all_items.append(frame)
                    item_labels.append(f"Frame {i+1}")
            
            # Add uploaded images if any (dynamic)
            if uploaded_images:
                from PIL import Image
                import io
                
                # Cache images in session_state to avoid re-reading
                current_img_names = [img.name for img in uploaded_images]
                previous_img_names = st.session_state.get('cached_img_names', [])
                
                if current_img_names != previous_img_names:
                    # New images uploaded, cache them
                    previous_img_count = len(previous_img_names)
                    current_img_count = len(current_img_names)
                    
                    cached_images = []
                    for img_file in uploaded_images:
                        img_file.seek(0)  # Reset file pointer
                        img_bytes = img_file.read()
                        img = Image.open(io.BytesIO(img_bytes))
                        cached_images.append(img)
                    st.session_state['cached_images'] = cached_images
                    st.session_state['cached_img_names'] = current_img_names
                    
                    # Smart selection for new images only
                    num_video_frames = len(st.session_state.get('video_frames', []))
                    if current_img_count > previous_img_count:
                        # New images added - select only the new ones
                        for i in range(num_video_frames + previous_img_count, num_video_frames + current_img_count):
                            st.session_state[f"frame_select_{i}"] = True
                
                # Use cached images
                for i, img in enumerate(st.session_state.get('cached_images', [])):
                    all_items.append(img)
                    item_labels.append(f"📷 {current_img_names[i]}")
            
            st.subheader(f"Select Items to Analyze ({len(all_items)} total)")
            if uploaded_images:
                st.caption(f"🎬 {len(st.session_state['video_frames'])} frames + 📷 {len(uploaded_images)} images")
            
            # Select All / Deselect All buttons
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Select All"):
                    for i in range(len(all_items)):
                        st.session_state[f"frame_select_{i}"] = True
                    st.rerun()
            with col_b:
                if st.button("Deselect All"):
                    for i in range(len(all_items)):
                        st.session_state[f"frame_select_{i}"] = False
                    st.rerun()
            
            # Create a grid for selection
            cols = st.columns(4)
            
            # Helper to initialize keys if not present (default to False - unselected)
            if 'frames_just_extracted' in st.session_state and st.session_state['frames_just_extracted']:
                 for i in range(len(all_items)):
                        st.session_state[f"frame_select_{i}"] = False
                 st.session_state['frames_just_extracted'] = False



            for i, item in enumerate(all_items):
                col = cols[i % 4]
                with col:
                    st.image(item, width="stretch")
                    # Layout pour Checkbox + Bouton Supprimer
                    c1, c2 = st.columns([0.8, 0.2])
                    with c1:
                        st.checkbox(
                            item_labels[i], 
                            key=f"frame_select_{i}"
                        )
                    with c2:
                        if st.button("🗑️", key=f"del_{i}", help="Remove this image"):
                            # Determine source and delete
                            num_video_frames = len(st.session_state.get('video_frames', []))
                            
                            if i < num_video_frames:
                                # It's a video frame
                                st.session_state['video_frames'].pop(i)
                                st.success("Frame removed!")
                            else:
                                # It's an uploaded image
                                img_idx = i - num_video_frames
                                if 'cached_images' in st.session_state:
                                    st.session_state['cached_images'].pop(img_idx)
                                    if 'cached_img_names' in st.session_state:
                                        st.session_state['cached_img_names'].pop(img_idx)
                                    st.success("Image removed!")
                            
                            # Clean up selection state for this index to avoid errors
                            if f"frame_select_{i}" in st.session_state:
                                del st.session_state[f"frame_select_{i}"]
                                
                            st.rerun()
                    
                    if show_weights:
                        st.slider(
                            "Weight",
                            min_value=0.0,
                            max_value=2.0,
                            value=st.session_state.get(f"weight_{i}", 1.0),
                            step=0.1,
                            key=f"weight_{i}",
                            label_visibility="collapsed"
                        )
                        st.caption(f"Weight: {st.session_state.get(f'weight_{i}', 1.0)}")
                        
                        # Granular Focus Selector
                        focus_options = [
                            "All Image",
                            "Character/Face",
                            "Pose/Body",
                            "Clothing",
                            "Background",
                            "Colors/Palette",
                            "Style/Ambiance"
                        ]
                        st.selectbox(
                            "Focus on:",
                            options=focus_options,
                            index=0,
                            key=f"focus_{i}",
                            label_visibility="collapsed"
                        )
                        st.caption(f"Focus: {st.session_state.get(f'focus_{i}', 'All Image')}")
            
            st.divider()
            
            # Calculate selected count dynamically for display
            current_selection_count = sum(1 for i in range(len(all_items)) if st.session_state.get(f"frame_select_{i}", False))
            st.caption(f"Selected: {current_selection_count} items")

    # Activity Log (Bottom of Sidebar)
    with st.sidebar:
        st.divider()
        st.caption("Activity Log")
        if 'video_frames' in st.session_state:
            st.success(f"✅ {len(st.session_state['video_frames'])} frames extracted")

# Analysis Section (Shown when frames are selected)
has_video = 'video_frames' in st.session_state and st.session_state['video_frames']
has_images = uploaded_images is not None and len(uploaded_images) > 0

if has_video or has_images:
    # Rebuild all_items and item_labels dynamically
    all_items = []
    item_labels = []
    
    if has_video:
        for i, frame in enumerate(st.session_state['video_frames']):
            all_items.append(frame)
            item_labels.append(f"Frame {i+1}")
    
    # Use cached images from session_state
    if 'cached_images' in st.session_state:
        cached_names = st.session_state.get('cached_img_names', [])
        for i, img in enumerate(st.session_state['cached_images']):
            all_items.append(img)
            name = cached_names[i] if i < len(cached_names) else "Image"
            item_labels.append(f"📷 {name}")
    

    # Activity Log (Bottom of Sidebar)
    with st.sidebar:
        st.divider()
        st.caption("Activity Log")
        if 'video_frames' in st.session_state:
            st.success(f"✅ {len(st.session_state['video_frames'])} frames extracted")

# Analysis Section (Shown when frames are selected)
has_video = 'video_frames' in st.session_state and st.session_state['video_frames']
has_images = uploaded_images is not None and len(uploaded_images) > 0

if has_video or has_images:
    # Rebuild all_items and item_labels dynamically
    all_items = []
    item_labels = []
    
    if has_video:
        for i, frame in enumerate(st.session_state['video_frames']):
            all_items.append(frame)
            item_labels.append(f"Frame {i+1}")
    
    # Use cached images from session_state
    if 'cached_images' in st.session_state:
        cached_names = st.session_state.get('cached_img_names', [])
        for i, img in enumerate(st.session_state['cached_images']):
            all_items.append(img)
            name = cached_names[i] if i < len(cached_names) else "Image"
            item_labels.append(f"📷 {name}")
    
    # Get selected items
    selected_indices = [i for i in range(len(all_items)) if st.session_state.get(f"frame_select_{i}", False)]
    
    st.divider()
    
    # Debug / Info
    st.caption(f"✅ **{len(selected_indices)} item(s) selected**")
    
    # Custom Instruction Input
    custom_instruction = st.text_area(
        "✨ Custom Instruction (Override)",
        placeholder="e.g., 'Make it cyberpunk', 'Focus on the eyes', 'Ignore the background'",
        help="Add specific instructions that will override the default prompt behavior.",
        height=68
    )

    # Action Buttons
    ac1, ac2, ac3 = st.columns(3)
    
    # 1. ANALYZE DIRECTLY
    with ac1:
        if st.button(f"🚀 Analyze", key="btn_analyze_direct", type="primary", use_container_width=True):
            if not selected_indices:
                st.warning("⚠️ Select items first!")
            else:
                selected_items = [all_items[i] for i in selected_indices]
                
                # Get Template
                mode_config = prompts["analysis_modes"][analysis_mode]
                template_str = mode_config["template"]
                
                # Render Template
                if analysis_mode == "style_transfer_pro":
                    from jinja2 import Template
                    prompt_text = Template(template_str).render(style=selected_style)
                else:
                    prompt_text = template_str
                
                # Inject Weights & Focus Info for fusion modes AND biometric modes (alt_pov, ultimate_biome_fashion_icon, etc.)
                # This allows granular control over which aspects to extract from each image
                biometric_modes = ["alt_pov", "ultimate_biome_fashion_icon", "experimental_fashion_lab", "biome_ultra_detailed"]
                if "fusion" in analysis_mode.lower() or analysis_mode in biometric_modes:
                    weights_info = []
                    
                    # Conflict Detection Lists
                    has_all_focus = False
                    has_clothing_focus = False
                    
                    for idx, real_idx in enumerate(selected_indices):
                        w = st.session_state.get(f"weight_{real_idx}", 1.0)
                        focus = st.session_state.get(f"focus_{real_idx}", "All Image")
                        
                        if focus == "All Image": has_all_focus = True
                        if focus == "Clothing": has_clothing_focus = True
                        
                        # Build info string
                        info_parts = []
                        if w != 1.0:
                            info_parts.append(f"Weight {w}")
                    
                    # USER WARNING FOR CONFLICT
                    if has_all_focus and has_clothing_focus:
                        st.warning("⚠️ **Logique Conflict Detected:** You have an image on 'All Image' and another on 'Clothing'. The 'All' image implies keeping its own clothing, which fights against your specific clothing source. **Tip:** Change the 'All' image to 'Face' or 'Pose' to let the Clothing source win.")
                    
                    # Reset loop for processing (cleaner than trying to merge loops perfectly with indices logic above complex block)
                    for idx, real_idx in enumerate(selected_indices):
                        w = st.session_state.get(f"weight_{real_idx}", 1.0)
                        focus = st.session_state.get(f"focus_{real_idx}", "All Image")
                        
                        # Build info string
                        info_parts = []
                        if w != 1.0:
                            info_parts.append(f"Weight {w}")

                        # HARDENED FOCUS RULES
                        if focus == "Character/Face":
                            focus_instruction = f"(STRICTLY EXTRACT FACE GEOMETRY & IDENTITY. IGNORE BACKGROUND. STOP ANALYSIS BELOW THE NECK. EXTRACT PRECISE HAIR STYLE & TEXTURE)"
                        elif focus == "Pose/Body":
                            focus_instruction = f"(STRICTLY EXTRACT POSE & BODY SHAPE. IGNORE FACE IDENTITY. IGNORE CLOTHING TEXTURE/DETAILS)"
                        elif focus == "Clothing":
                            focus_instruction = f"(STRICTLY EXTRACT OUTFIT DETAILS/FABRIC. IGNORE FACE. IGNORE POSE. **IGNORE HAIR** - Hair belongs to Face Source!)"
                        elif focus == "Background":
                            focus_instruction = f"(STRICTLY EXTRACT ENVIRONMENT. IGNORE SUBJECT)"
                        elif focus == "All Image":
                             focus_instruction = "(Extract EVERYTHING: Face, Pose, Clothing, Background)"
                        else:
                            focus_instruction = f"(Focus on {focus})"
                        
                        info_parts.append(f"Focus: {focus} {focus_instruction}")

                        # Always add the image line
                        weights_info.append(f"- Image {idx+1}: {', '.join(info_parts)}")
                    
                    if weights_info:
                        weight_context = "\n\n**USER ASSIGNED WEIGHTS & FOCUS:**\n" + "\n".join(weights_info) + "\n\n"
                        
                        # GLOBAL PRIORITY RULE FOR FUSION
                        priority_rule = """
**⚡ FUSION PRIORITY PROTOCOL (STRICT IDENTITY):**
1. For **FACE/HEAD/HAIR** details: Use ONLY the image marked "Focus: Face". **This Focus OVERRIDES strict weights.** If Image 1 is "Face", Face 1 represents the identity.
2. For **BODY/POSE/CLOTHING** details: Use ONLY images marked "Focus: Pose" or "Focus: Clothing". 
   **⛔ CRITICAL:** DO NOT use the "Face" image for Body/Clothing description (unless 'All Image' is set).
"""
                        prompt_text = weight_context + priority_rule + prompt_text
                
                # Inject ALT POV Selection
                if analysis_mode == "alt_pov" and 'alt_pov_selection' in st.session_state and st.session_state['alt_pov_selection']:
                    selected_looks_str = ", ".join(st.session_state['alt_pov_selection'])
                    # Extract look numbers for clarity
                    look_numbers = [look.split(".")[0] for look in st.session_state['alt_pov_selection']]
                    
                    selection_instruction = f"""

🚨 **CRITICAL OVERRIDE - MANDATORY:**
You MUST generate ONLY the following looks: {selected_looks_str}

**DO NOT GENERATE** any other looks (skip looks not in this list).
**START IMMEDIATELY** with the first selected look. Do NOT process or mention unselected looks.
**IGNORE** all look definitions except the ones listed above.

This is a HARD CONSTRAINT. Generating unselected looks is FORBIDDEN.
"""
                    prompt_text = prompt_text + selection_instruction
                
                # Inject Look Fidelity for alt_pov
                if analysis_mode == "alt_pov" and 'look_fidelity' in st.session_state:
                    fidelity = st.session_state['look_fidelity']
                    
                    # Determine mode based on fidelity value
                    if fidelity <= 45:
                        mode_name = "SOURCE DOMINANT"
                        primary_rule = "YOU MUST KEEP the Source Clothing/Pose. **CRITICAL:** Use the Fusion Focus/Weights to decide WHICH source image provides the clothing (e.g., if Image 2 is 'Focus: Clothing', use Image 2's outfit). The LOOK provides ONLY lighting/color inspiration."
                        example = "Source: Image 1 (Face) + Image 2 (Clothing) → OUTPUT: Person with Face 1 wearing Outfit 2, with LOOK's lighting."
                    elif fidelity <= 75:
                        mode_name = "BALANCED BLEND"
                        primary_rule = "BLEND the LOOK outfit with the Source Clothing (determined by Fusion Focus/Weights). ADAPT the LOOK pose to the source pose."
                        example = "Source: Image 1 (Face) + Image 2 (Clothing) → OUTPUT: Outfit 2 blended with LOOK style, Face 1."
                    elif fidelity <= 85:
                        mode_name = "LOOK DOMINANT"
                        primary_rule = "APPLY the LOOK's outfit and pose. Extract ONLY biometrics (face, body) from source."
                        example = "Source: woman in jeans standing → OUTPUT: woman in latex catsuit straddling chrome chair (LOOK wins)"
                    else:
                        mode_name = "PURE LOOK"
                        primary_rule = "STRICT LOOK APPLICATION. Source = face/body measurements ONLY. Completely ignore source clothing/pose/setting."
                        example = "Source: ANY outfit/pose → OUTPUT: EXACT LOOK definition with source's face"
                    
                    fidelity_instruction = f"""

═══════════════════════════════════════════════════════════════
🚨 CRITICAL OVERRIDE - LOOK FIDELITY MODE: {mode_name} ({fidelity}%)
═══════════════════════════════════════════════════════════════

**MANDATORY RULE:**
{primary_rule}

**CONCRETE EXAMPLE:**
{example}

**FORBIDDEN ACTIONS at {fidelity}%:**
"""
                    
                    if fidelity <= 45:
                        fidelity_instruction += f"""
- ❌ DO NOT change the source clothing (keep jeans if source has jeans)
- ❌ DO NOT change the source pose (keep standing if source is standing)
- ❌ DO NOT invent new outfits from LOOK definitions
- ✅ DO apply LOOK's lighting style and color palette to the source scene
"""
                    elif fidelity <= 75:
                        fidelity_instruction += f"""
**HYBRID LOGIC:** Source STRUCTURE + Look MATERIAL.
- ❌ DO NOT replace the item type (e.g. if Source is T-Shirt, output T-Shirt)
- ✅ DO apply Look's FABRIC/TEXTURE/COLOR to the Source item (e.g. Source T-Shirt -> becomes Lace/Latex T-Shirt).
- Mix Ratio: {fidelity}% Look Influence on styling.
"""
                    elif fidelity <= 85:
                        fidelity_instruction += """
- ❌ DO NOT keep source clothing (replace with LOOK outfit)
- ❌ DO NOT keep source pose (replace with LOOK pose)
- ✅ DO keep source biometrics (face, body measurements)
- ✅ DO apply LOOK's outfit, pose, lighting, POV
"""
                    else:
                        fidelity_instruction += """
- ❌ DO NOT reference source clothing AT ALL
- ❌ DO NOT reference source pose AT ALL
- ❌ DO NOT reference source setting AT ALL
- ✅ DO extract ONLY face shape, body measurements from source
- ✅ DO apply 100% of LOOK definition (outfit, pose, lighting, POV)
"""
                    
                    fidelity_instruction += f"""

**VERIFICATION CHECKLIST before generating:**
□ Have I applied the LOOK at {fidelity}% strictness?
□ Does my output match the {mode_name} mode rules above?
□ Have I avoided the FORBIDDEN actions listed?

IF YOU IGNORE THIS INSTRUCTION, THE OUTPUT WILL BE REJECTED.

**REQUIRED OUTPUT STRUCTURE (STRICT):**

## 🚀 FINAL PROMPT (COPY THIS)
```markdown
[AESTHETIC]: (Start with "Photorealistic shot of...", "Cinematic portrait of...". Define the Style & Realism here.)

[LOOK DESCRIPTION]: (The Main Subject: Outfit, Pose, Action, Environment. VISUAL ONLY.)

[MODEL SPECS]: (Paste FULLY EXPANDED biometric details. MUST include "visible skin texture", "pores", "vellus hair". **CRITICAL FOR EYES:** Replace any "vivid/intense/electric" descriptors with "soft/muted/deep" to ensure realism.)

[TECHNICAL]: (Lighting, Color Grading, 8k. **DO NOT mention EQUIPMENT names (Camera, Softbox, Spotlight, Flash, Lens).** DESCRIBE LIGHT/VISUALS ONLY (e.g. "soft diffused light", "rim lighting", "bokeh").)
```
(All content must be inside this single code block)

═══════════════════════════════════════════════════════════════
"""
                    prompt_text = prompt_text + fidelity_instruction

                # Inject Custom Instruction (Override)
                if custom_instruction and custom_instruction.strip():
                    override_text = f"\n\n⚠️ **IMPORTANT USER OVERRIDE / CUSTOM INSTRUCTION:**\n{custom_instruction.strip()}\n(This instruction takes PRIORITY over all previous instructions.)\n"
                    prompt_text = prompt_text + override_text

                st.info(f"**Prompt:** {prompt_text[:100]}...")
                
                try:
                    # Dependency Injection: The adapter is now interchangeable
                    # In a full DI framework, we would get this from a container
                    adapter = OllamaAdapter(
                        model_name=selected_model,
                        temperature=temperature
                    )
                    
                    result_container = st.empty()
                    full_response = ""
                    
                    # The app doesn't know which model it is, it just knows it's an AIModel
                    for chunk in adapter.analyze(selected_items, prompt_text, stream=True):
                        full_response += chunk
                        result_container.markdown(full_response + "▌")
                    
                    result_container.markdown(full_response)
                    st.success("✅ Analysis Complete!")
                    
                    
                    # Parse response using ResultAdapter
                    from core.result_adapter import ResultAdapter
                    
                    adapter_parser = ResultAdapter()
                    parsed = adapter_parser.parse_response(full_response, analysis_mode)
                    
                    # Store in session state to persist across reruns
                    st.session_state['last_analysis'] = {
                        'prompts': parsed['prompts'],
                        'json_data': parsed['json_data'],
                        'mode': analysis_mode,
                        'style': selected_style,
                        'model': selected_model,
                        'items': selected_items
                    }
                    
                    # Display parsed prompts
                    if parsed['prompts']:
                        st.divider()
                        st.markdown("### 📋 **COPY-READY PROMPTS**")
                        st.caption("💡 Final prompts are shown first (expanded). Intermediate analysis is below (collapsed).")
                        
                        # Separate prompts into final and intermediate
                        final_prompts = []
                        intermediate_prompts = []
                        
                        for i, (title, content) in enumerate(parsed['prompts']):
                            title_lower = title.lower()
                            is_final = any(x in title_lower for x in ['unified', 'final', 'reproduction', 'prompt', 'look', 'variant'])
                            is_intermediate = any(x in title_lower for x in ['logic', 'reasoning', 'analysis', 'layer', 'json'])
                            
                            if is_final or (not is_intermediate):
                                final_prompts.append((i, title, content, True))  # (index, title, content, should_expand)
                            else:
                                intermediate_prompts.append((i, title, content, False))
                        
                        # Display final prompts first, then intermediate
                        all_ordered_prompts = final_prompts + intermediate_prompts
                        
                        # Special case: If there are very few prompts (e.g. 1 or 2), expand all
                        if len(parsed['prompts']) <= 2:
                            all_ordered_prompts = [(i, t, c, True) for i, t, c, _ in all_ordered_prompts]
                        
                        for i, title, content, should_expand in all_ordered_prompts:
                            with st.expander(f"**{title}**", expanded=should_expand):
                                # Use text_area for better visibility and "whole prompt" view
                                # Calculate height based on content length (approx)
                                st.code(content, language="markdown")
                                
                                # Info and download button
                                col1, col2 = st.columns([2, 1])
                                with col1:
                                    st.caption(f"✨ {len(content)} characters")
                                with col2:
                                    # Create file content with metadata footer
                                    import datetime
                                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                    file_timestamp = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
                                    
                                    # Extract a short title
                                    title_words = title.split()[:5]
                                    short_title = "_".join(title_words).lower()
                                    short_title = "".join(c if c.isalnum() or c == "_" else "" for c in short_title)
                                    
                                    filename = f"{short_title}_{file_timestamp}.txt"
                                    
                                    metadata_footer = f"""

# ========================================
# GENERATION INFO
# ========================================
# Generated: {timestamp}
# Analysis Mode: {analysis_mode}
"""
                                    if selected_style:
                                        metadata_footer += f"# Style: {selected_style}\n"
                                    
                                    metadata_footer += "# ========================================\n"
                                    
                                    file_content = content + metadata_footer
                                    
                                    st.download_button(
                                        label="💾 Download .txt",
                                        data=file_content,
                                        file_name=filename,
                                        mime="text/plain",
                                        key=f"download_btn_{i}",
                                        use_container_width=True
                                    )
                                
                                # --- DATASET SAVING UI ---
                                st.divider()
                                st.caption("🧠 **Add to Training Dataset**")
                                # Give more space to rating column to prevent wrapping
                                c_rate, c_comment, c_btn = st.columns([3, 2, 1])
                                
                                with c_rate:
                                    # Star rating (1-5)
                                    rating = st.feedback("stars", key=f"rating_{i}")
                                    
                                with c_comment:
                                    comment = st.text_input("Comment (optional)", placeholder="e.g. Perfect lighting, bad hands...", key=f"comment_{i}", label_visibility="collapsed")
                                    
                                with c_btn:
                                    if st.button("💾", key=f"save_db_{i}", use_container_width=True):
                                        # Determine reference image name
                                        ref_image = "unknown"
                                        if selected_items and isinstance(selected_items[0], str):
                                            ref_image = os.path.basename(selected_items[0])
                                        elif 'video_frames' in st.session_state:
                                            ref_image = "video_frame_extraction"
                                            
                                        # Save with rating (0-4 from feedback widget -> 1-5)
                                        final_rating = (rating + 1) if rating is not None else 0
                                        
                                        db.save_analysis(
                                            image_name=ref_image,
                                            mode=analysis_mode,
                                            style=selected_style,
                                            model=selected_model,
                                            prompt_content=content,
                                            rating=final_rating,
                                            comment=comment
                                        )
                                        st.toast(f"✅ Saved with {final_rating} stars!", icon="💾")
                    
                    # Display JSON data for biometric modes
                    if parsed['json_data']:
                        import datetime
                        
                        # Generate Timestamp ID
                        ts = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
                        filename = f"biome_ID_{ts}.json"
                        
                        # Update ID in JSON to match
                        if isinstance(parsed['json_data'], dict):
                            parsed['json_data']["id"] = f"ID_{ts}"
                        
                        st.divider()
                        st.subheader("🧬 Biometric Data Extracted")
                        
                        # Visual Inspector
                        with st.expander("🔍 Inspect Raw JSON Data", expanded=False):
                            st.json(parsed['json_data'])
                        
                        # Offer download
                        st.download_button(
                            label=f"📥 Download {filename}",
                            data=json.dumps(parsed['json_data'], indent=2),
                            file_name=filename,
                            mime="application/json",
                            type="primary"
                        )
                    elif analysis_mode in ["ultimate_biome_fashion_icon", "fetish_mode_shorts", "biome_ultra_detailed"]:
                        st.warning("⚠️ No JSON block found in the response.")
                    
                except Exception as e:
                    st.error(f"Analysis Error: {str(e)}")

    # Display last analysis results (persists across reruns)
    if 'last_analysis' in st.session_state:
        last = st.session_state['last_analysis']
        
        st.divider()
        st.subheader("📊 Last Analysis Results")
        st.caption(f"Mode: {last['mode']} | Style: {last.get('style', 'N/A')} | Model: {last['model']}")
        
        # Display prompts
        if last['prompts']:
            for i, (title, content) in enumerate(last['prompts']):
                # Determine if this is a "Final" or "Important" prompt to expand by default
                title_lower = title.lower()
                is_final = any(x in title_lower for x in ['unified', 'final', 'reproduction', 'prompt', 'look', 'variant'])
                is_intermediate = any(x in title_lower for x in ['logic', 'reasoning', 'analysis', 'layer', 'json'])
                
                should_expand = is_final or (not is_intermediate)
                if len(last['prompts']) <= 2:
                    should_expand = True

                # SPECIAL DISPLAY FOR ALT_POV (SMART TABS)
                if last['mode'] == 'alt_pov' and "LOOK 1:" in content:
                    with st.expander(f"**{title} (28 LOOKS - SMART VIEW)**", expanded=should_expand):
                        st.info("✨ 28 Looks Detected - Organized by Mood")
                        
                        # Split content into Intro (JSON) and Looks
                        parts = content.split("**LOOK 1:")
                        intro = parts[0]
                        looks_content = "**LOOK 1:" + parts[1] if len(parts) > 1 else content
                        
                        # Display Intro/JSON first
                        with st.expander("🧬 Biometric Data & Intro", expanded=False):
                            st.code(intro, language="markdown")

                        # Create Tabs
                        tab_dark, tab_tech, tab_color, tab_light, tab_bonus, tab_fetish = st.tabs([
                            "🌑 DARK (1-5)", 
                            "🔌 TECH (6-10)", 
                            "🌈 COLOR (11-15)", 
                            "✨ LIGHT (16-20)",
                            "🔥 BONUS (21-22)",
                            "💋 FETISH (23-28)"
                        ])
                        
                        # Helper to extract look content
                        import re
                        def get_look(text, num):
                            pattern = f"\\*\\*LOOK {num}:(.*?)(?=\\*\\*LOOK {num+1}:|$)"
                            match = re.search(pattern, text, re.DOTALL)
                            return f"**LOOK {num}:{match.group(1)}" if match else ""

                        # Populate Tabs
                        with tab_dark:
                            for i in range(1, 6):
                                lk = get_look(looks_content, i)
                                if lk: 
                                    st.text_area(f"edit_{i}", value=lk.strip(), height=150, label_visibility="collapsed")
                                    st.code(lk.strip(), language="markdown")
                        
                        with tab_tech:
                            for i in range(6, 11):
                                lk = get_look(looks_content, i)
                                if lk: 
                                    st.text_area(f"edit_{i}", value=lk.strip(), height=150, label_visibility="collapsed")
                                    st.code(lk.strip(), language="markdown")
                                
                        with tab_color:
                            for i in range(11, 16):
                                lk = get_look(looks_content, i)
                                if lk: 
                                    st.text_area(f"edit_{i}", value=lk.strip(), height=150, label_visibility="collapsed")
                                    st.code(lk.strip(), language="markdown")
                                
                        with tab_light:
                            for i in range(16, 21):
                                lk = get_look(looks_content, i)
                                if lk: 
                                    st.text_area(f"edit_{i}", value=lk.strip(), height=150, label_visibility="collapsed")
                                    st.code(lk.strip(), language="markdown")
                        
                        with tab_bonus:
                            for i in range(21, 23):
                                lk = get_look(looks_content, i)
                                if lk: 
                                    st.text_area(f"edit_{i}", value=lk.strip(), height=150, label_visibility="collapsed")
                                    st.code(lk.strip(), language="markdown")
                        
                        with tab_fetish:
                            for i in range(23, 29):
                                lk = get_look(looks_content, i)
                                if lk: 
                                    st.text_area(f"edit_{i}", value=lk.strip(), height=150, label_visibility="collapsed")
                                    st.code(lk.strip(), language="markdown")

                        # Full Text Fallback (hidden by default)
                        with st.expander("📜 View Full Raw Output", expanded=False):
                            st.code(content, language="markdown")

                # STANDARD DISPLAY FOR OTHER MODES
                else:
                    with st.expander(f"**{title}**", expanded=should_expand):
                        # 1. READABLE VIEW (Wrapped Text)
                        st.caption("📖 **Read / Edit:**")
                        st.text_area(
                            label=f"preview_{i}", 
                            value=content, 
                            height=300, 
                            label_visibility="collapsed",
                            disabled=False # Allow minor manual edits if needed before copying? Or keep True? User often wants to tweak.
                        )
                        
                        # 2. COPY VIEW (One-Click)
                        st.caption("📋 **Copy Block:**")
                        st.code(content, language="markdown")
                    
                    col1, col2 = st.columns([2, 1])
                    with col1:
                        st.caption(f"✨ {len(content)} characters")
                    with col2:
                        import datetime
                        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        file_timestamp = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
                        
                        title_words = title.split()[:5]
                        short_title = "_".join(title_words).lower()
                        short_title = "".join(c if c.isalnum() or c == "_" else "" for c in short_title)
                        filename = f"{short_title}_{file_timestamp}.txt"
                        
                        metadata_footer = f"""

# ========================================
# GENERATION INFO
# ========================================
# Generated: {timestamp}
# Analysis Mode: {last['mode']}
# ========================================
"""
                        
                        file_content = content + metadata_footer
                        
                        st.download_button(
                            label="💾 Download .txt",
                            data=file_content,
                            file_name=filename,
                            mime="text/plain",
                            key=f"persist_download_{i}",
                            use_container_width=True
                        )
                    
                    # Dataset saving UI
                    st.divider()
                    st.caption("🧠 **Add to Training Dataset**")
                    c_rate, c_comment, c_btn = st.columns([3, 2, 1])
                    
                    with c_rate:
                        rating = st.feedback("stars", key=f"persist_rating_{i}")
                    with c_comment:
                        comment = st.text_input("Comment (optional)", placeholder="e.g. Perfect lighting...", key=f"persist_comment_{i}", label_visibility="collapsed")
                    with c_btn:
                        if st.button("💾", key=f"persist_save_{i}", use_container_width=True):
                            ref_image = "unknown"
                            if last['items'] and isinstance(last['items'][0], str):
                                ref_image = os.path.basename(last['items'][0])
                            elif 'video_frames' in st.session_state:
                                ref_image = "video_frame_extraction"
                            
                            final_rating = (rating + 1) if rating is not None else 0
                            
                            db.save_analysis(
                                image_name=ref_image,
                                mode=last['mode'],
                                style=last.get('style'),
                                model=last['model'],
                                prompt_content=content,
                                rating=final_rating,
                                comment=comment
                            )
                            st.toast(f"✅ Saved with {final_rating} stars!", icon="💾")
        
        # Display JSON if exists
        if last.get('json_data'):
            import datetime
            ts = datetime.datetime.now().strftime("%d%m%Y%H%M%S")
            filename = f"biome_ID_{ts}.json"
            
            st.divider()
            st.subheader("🧬 Biometric Data Extracted")
            
            with st.expander("🔍 Inspect Raw JSON Data", expanded=False):
                st.json(last['json_data'])
            
            st.download_button(
                label=f"📥 Download {filename}",
                data=json.dumps(last['json_data'], indent=2),
                file_name=filename,
                mime="application/json",
                type="primary",
                key="persist_json_download"
            )



    # 2. SAVE TO DISK
    with ac2:
        if st.button(f"💾 Save", key="btn_save_direct", use_container_width=True):
            if not selected_indices:
                st.warning("⚠️ Select items first!")
            else:
                import os
                import time
                
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                save_dir = f"saved_collections/selection_{timestamp}"
                os.makedirs(save_dir, exist_ok=True)
                
                for i in selected_indices:
                    item = all_items[i]
                    label = item_labels[i]
                    safe_label = "".join([c for c in label if c.isalnum() or c in (' ', '.', '_')]).strip()
                    filename = f"{i+1:03d}_{safe_label}.png"
                    item.save(os.path.join(save_dir, filename))
                
                st.success(f"✅ Saved to `{save_dir}`")

    # 3. ADD TO COLLECTION
    with ac3:
        pass

# ---------------------------------------------------------
# COLLECTION SECTION
# ---------------------------------------------------------

# ---------------------------------------------------------
# HISTORY SECTION
# ---------------------------------------------------------
st.divider()
st.header("📜 Recent History")

try:
    history = db.get_history(limit=10)
    if not history:
        st.info("No history yet. Start analyzing!")
    else:
        for item in history:
            # Create a nice title for the expander
            stars = "⭐" * item['rating'] if item['rating'] > 0 else ""
            style_info = f" | {item['style']}" if item['style'] else ""
            title = f"📅 {item['timestamp']} {stars} - {item['mode']}{style_info}"
            
            with st.expander(title):
                if item['comment']:
                    st.info(f"📝 **Note:** {item['comment']}")
                st.caption(f"🖼️ Image: {item['image_name']} | 🤖 Model: {item['model']}")
                st.code(item['prompt_content'], language='text')
                
                # Download and Delete buttons
                col_dl, col_del = st.columns([3, 1])
                with col_dl:
                    st.download_button(
                        label="💾 Download Again",
                        data=item['prompt_content'],
                        file_name=f"history_prompt_{item['id']}.txt",
                        mime="text/plain",
                        key=f"hist_dl_{item['id']}"
                    )
                with col_del:
                    if st.button("🗑️ Delete", key=f"hist_del_{item['id']}", type="secondary", use_container_width=True):
                        db.delete_analysis(item['id'])
                        st.toast("🗑️ Deleted from history", icon="✅")
                        st.rerun()
except Exception as e:
    st.error(f"Could not load history: {e}")
