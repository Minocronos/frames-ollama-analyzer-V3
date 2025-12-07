import streamlit as st
import yaml
import os
from pathlib import Path
from core.video_processor import VideoProcessor
from core.gemini_adapter import GeminiAdapter
# from ui.components import render_flow_graph  # Temporarily disabled
from jinja2 import Template
import ollama

# Page Config (Must be first)
st.set_page_config(
    page_title="Gemini 3 Analyser",
    page_icon="👁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Config
def load_config():
    with open("config/settings.yaml", "r", encoding="utf-8") as f:
        settings = yaml.safe_load(f)
    with open("config/prompts.yaml", "r", encoding="utf-8") as f:
        prompts = yaml.safe_load(f)
    return settings, prompts

settings, prompts = load_config()

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
    st.title("👁️ Gemini 3 Analyser")
    
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
        help="Choose whether to analyze video frames, uploaded images, or both combined."
    )
    
    st.header("Configuration")
    analysis_mode = st.selectbox(
        "Analysis Mode",
        options=list(prompts["analysis_modes"].keys()),
        format_func=lambda x: x.replace("_", " ").title(),
        help="Choose how Gemini should analyze the frames."
    )
    
    # Show description of selected mode
    mode_description = prompts["analysis_modes"][analysis_mode].get("description", "")
    if mode_description:
        st.info(f"ℹ️ {mode_description}")
    
    if analysis_mode == "creative_conversion":
        selected_style = st.selectbox("Style", prompts["styles"])
    else:
        selected_style = None
        
    st.divider()
    st.caption("Pipeline Visualization")
    # render_flow_graph(analysis_mode, selected_style)  # Temporarily disabled
    st.info("Flow graph temporarily disabled")
    
    st.divider()
    st.info("Hot-Reload Active: Edit `prompts.yaml` to see changes instantly.")

# Main Content
st.title("Video Intelligence & Art")
st.markdown("Upload a video to unleash the reasoning power of **Gemini 3**.")

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
    st.session_state['all_frames'] = all_frames
    st.session_state['frame_sources'] = ['image'] * len(all_frames)
    
    # Display images in grid
    st.subheader(f"📷 {len(all_frames)} Image(s) Ready")
    cols = st.columns(4)
    for i, img in enumerate(all_frames):
        with cols[i % 4]:
            st.image(img, use_container_width=True)
            st.caption(f"Image {i+1}")
    
    # Direct analysis button
    st.divider()
    if st.button("🚀 Analyze Images", type="primary", use_container_width=True):
        # Get Template
        mode_config = prompts["analysis_modes"][analysis_mode]
        template_str = mode_config["template"]
        
        # Render Template
        if analysis_mode == "creative_conversion":
            from jinja2 import Template
            prompt_text = Template(template_str).render(style=selected_style)
        else:
            prompt_text = template_str
        
        st.info(f"**Prompt:** {prompt_text[:100]}...")
        
        # Run Analysis
        try:
            from core.gemini_adapter import GeminiAdapter
            adapter = GeminiAdapter(
                model_name=selected_model,
                temperature=settings['model']['temperature']
            )
            
            result_container = st.empty()
            full_response = ""
            
            for chunk in adapter.analyze(all_frames, prompt_text, stream=True):
                full_response += chunk
                result_container.markdown(full_response + "▌")
            
            # Store result in session state
            st.session_state['analysis_result'] = full_response
            result_container.markdown(full_response)
            st.success("✅ Analysis Complete!")
            
        except Exception as e:
            st.error(f"Analysis Error: {str(e)}")
    
    # Display stored result if exists
    if 'analysis_result' in st.session_state and st.session_state['analysis_result']:
        st.divider()
        st.subheader("📝 Analysis Result")
        st.markdown(st.session_state['analysis_result'])

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
                
                # Save uploaded file temporarily
                temp_path = f"temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Extract frames
                frames = processor.extract_frames(
                    temp_path,
                    interval=interval,
                    max_frames=max_frames
                )
                
                # Clean up
                os.remove(temp_path)
                
                # Store in session state
                st.session_state['extracted_frames'] = frames
                st.session_state['frames_just_extracted'] = True # Flag to reset selection
                st.success(f"✅ Extracted {len(frames)} frames")
                st.rerun()
    
    with col2:
        if 'extracted_frames' in st.session_state and st.session_state['extracted_frames']:
            st.subheader("Select Frames to Analyze")
            
            frames = st.session_state['extracted_frames']
            
            # Select All / Deselect All buttons
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("Select All"):
                    for i in range(len(frames)):
                        st.session_state[f"frame_select_{i}"] = True
                    st.rerun()
            with col_b:
                if st.button("Deselect All"):
                    for i in range(len(frames)):
                        st.session_state[f"frame_select_{i}"] = False
                    st.rerun()
            
            # Create a grid for selection
            cols = st.columns(4) # 4 columns for better density
            
            # Helper to initialize keys if not present (default to False - unselected)
            # We use a separate flag to know if it's a fresh extraction
            if 'frames_just_extracted' in st.session_state and st.session_state['frames_just_extracted']:
                 for i in range(len(frames)):
                        st.session_state[f"frame_select_{i}"] = False
                 st.session_state['frames_just_extracted'] = False

            for i, frame in enumerate(frames):
                col = cols[i % 4]
                with col:
                    st.image(frame, use_container_width=True)
                    # Checkbox directly bound to session state key
                    st.checkbox(
                        f"Frame {i+1}", 
                        key=f"frame_select_{i}",
                        value=st.session_state.get(f"frame_select_{i}", False)
                    )
            
            st.divider()
            
            # Calculate selected count dynamically for display
            current_selection_count = sum(1 for i in range(len(frames)) if st.session_state.get(f"frame_select_{i}", False))
            st.caption(f"Selected: {current_selection_count} frames")

    # Activity Log (Bottom of Sidebar)
    with st.sidebar:
        st.divider()
        st.caption("Activity Log")
        if 'extracted_frames' in st.session_state:
            st.success(f"✅ {len(st.session_state['extracted_frames'])} frames extracted")

# Analysis Section (Shown when frames are selected)
if 'extracted_frames' in st.session_state and st.session_state['extracted_frames']:
    frames = st.session_state['extracted_frames']
    
    # Get selected frames
    selected_indices = [i for i in range(len(frames)) if st.session_state.get(f"frame_select_{i}", False)]
    
    if selected_indices:
        st.divider()
        st.subheader("Analysis")
        
        if st.button(f"🚀 Analyze {len(selected_indices)} Selected Frame(s)", type="primary", use_container_width=True):
            selected_frames = [frames[i] for i in selected_indices]
            
            # Get Template
            mode_config = prompts["analysis_modes"][analysis_mode]
            template_str = mode_config["template"]
            
            # Render Template
            if analysis_mode == "creative_conversion":
                from jinja2 import Template
                prompt_text = Template(template_str).render(style=selected_style)
            else:
                prompt_text = template_str
            
            st.info(f"**Prompt:** {prompt_text[:100]}...")
            
            # Run Analysis
            try:
                adapter = GeminiAdapter(
                    model_name=selected_model,
                    temperature=settings['model']['temperature']
                )
                
                result_container = st.empty()
                full_response = ""
                
                for chunk in adapter.analyze(selected_frames, prompt_text, stream=True):
                    full_response += chunk
                    result_container.markdown(full_response + "▌")
                
                result_container.markdown(full_response)
                st.success("✅ Analysis Complete!")
                
            except Exception as e:
                st.error(f"Analysis Error: {str(e)}")
