import gradio as gr
import cv2
import os
import shutil
import numpy as np
import toml
from modules.ollama_frame_analyzer import ollama_frame_analyzer_ui

# Global variable to store all extracted frame paths
all_extracted_frame_paths = []

# Load prompts from TOML file
PROMPTS_FILE = "prompts/default_analysis_prompt.toml"
try:
    with open(PROMPTS_FILE, 'r', encoding='utf-8') as f:
        config = toml.load(f)
    prompt_choices = ["", *list(config['prompts'].values())]
    default_prompt_value = prompt_choices[0] if prompt_choices else ""
    print(f"✅ {len(prompt_choices)-1} prompts chargés depuis {PROMPTS_FILE}")
except Exception as e:
    print(f"❌ Erreur chargement prompts: {e}")
    prompt_choices = ["Décris l'image", "Identifie les objets", "Analyse l'activité"]
    default_prompt_value = "Décris l'image"

def extract_frames(video_path, interval):
    """
    Extracts frames from a video file at a given interval.
    """
    global all_extracted_frame_paths
    print(f"--- Début de l'extraction ---")
    print(f"Chemin de la vidéo: {video_path}")
    print(f"Intervalle: {interval}")

    if not video_path:
        all_extracted_frame_paths = []
        return [], gr.CheckboxGroup(choices=[]) # Return two empty lists

    output_dir = "temp_frames"
    os.makedirs(output_dir, exist_ok=True)

    for f in os.listdir(output_dir):
        os.remove(os.path.join(output_dir, f))

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Erreur: Impossible d'ouvrir la vidéo.")
        all_extracted_frame_paths = []
        return [], gr.CheckboxGroup(choices=[])

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Propriétés de la vidéo: {width}x{height}, {fps:.2f} FPS, {total_frames} frames totales")

    if total_frames == 0:
        print("Erreur: La vidéo semble n'avoir aucune frame.")
        cap.release()
        all_extracted_frame_paths = []
        return [], gr.CheckboxGroup(choices=[])

    frame_count = 0
    saved_frame_count = 0
    frame_paths = []
    checkbox_choices = [] # New list for checkbox choices

    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"Fin de la lecture à la frame {frame_count}.")
            break

        if frame_count % int(interval) == 0:
            if np.mean(frame) < 10:
                print(f"Frame {frame_count} semble noire.")

            frame_filename = os.path.join(output_dir, f"frame_{saved_frame_count:04d}.png")
            cv2.imwrite(frame_filename, frame)
            
            # Resize frame if too large
            frame_filename = resize_image_if_needed(frame_filename)
            
            frame_paths.append(frame_filename)
            checkbox_choices.append((f"Frame {saved_frame_count}", frame_filename)) # Add label and value

            saved_frame_count += 1

        frame_count += 1

    cap.release()
    print(f"{saved_frame_count} frames extraites.")
    print(f"--- Fin de l'extraction ---")
    
    all_extracted_frame_paths = frame_paths # Store all paths globally
    return frame_paths, gr.update(choices=checkbox_choices, value=[]) # Return gallery and checkbox group choices and empty value

def resize_image_if_needed(image_path, max_size=(1024, 1024), max_file_size_mb=5):
    """
    Resize image if it's too large for API processing.
    Returns the path to the processed image (original or resized).
    """
    try:
        # Check file size first (stricter limit)
        file_size_mb = os.path.getsize(image_path) / (1024 * 1024)
        if file_size_mb > max_file_size_mb:
            print(f"Image trop grande ({file_size_mb:.1f}MB > {max_file_size_mb}MB), redimensionnement forcé...")
        else:
            # Check dimensions (stricter limits)
            img = cv2.imread(image_path)
            if img is None:
                return image_path
                
            height, width = img.shape[:2]
            if width <= max_size[0] and height <= max_size[1]:
                return image_path  # No resize needed
        
        # Load and resize with more aggressive settings
        img = cv2.imread(image_path)
        if img is None:
            print(f"Impossible de lire l'image pour redimensionner: {image_path}")
            return image_path
            
        height, width = img.shape[:2]
        
        # More aggressive resize: ensure both dimensions are within limits
        if width > max_size[0] or height > max_size[1]:
            ratio = min(max_size[0] / width, max_size[1] / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            
            # Resize with higher quality interpolation
            resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_LANCZOS4)
            
            # Compress more aggressively
            base_name = os.path.splitext(os.path.basename(image_path))[0]
            resized_path = os.path.join(os.path.dirname(image_path), f"{base_name}_resized.jpg")
            
            # Save with JPEG compression to reduce size
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 85]  # 85% quality
            cv2.imwrite(resized_path, resized_img, encode_param)
            
            final_size_mb = os.path.getsize(resized_path) / (1024 * 1024)
            print(f"Image redimensionnée: {width}x{height} -> {new_width}x{new_height}, taille: {final_size_mb:.1f}MB")
            return resized_path
            
        return image_path
        
    except Exception as e:
        print(f"Erreur lors du redimensionnement: {e}")
        return image_path

def process_photos(photo_files):
    """
    Process uploaded photo files and return them as frames.
    """
    global all_extracted_frame_paths
    print(f"--- Début du traitement des photos ---")
    print(f"Nombre de photos: {len(photo_files) if photo_files else 0}")

    if not photo_files:
        all_extracted_frame_paths = []
        return [], gr.CheckboxGroup(choices=[])

    output_dir = "temp_frames"
    os.makedirs(output_dir, exist_ok=True)

    for f in os.listdir(output_dir):
        os.remove(os.path.join(output_dir, f))

    frame_paths = []
    checkbox_choices = []

    for i, photo_file in enumerate(photo_files):
        # Gradio file objects have a .name attribute with the temp file path
        if hasattr(photo_file, 'name'):
            photo_path = photo_file.name
            photo_name = os.path.basename(photo_path)
        else:
            # Fallback for other formats
            photo_path = str(photo_file)
            photo_name = f"photo_{i}"
        
        print(f"Traitement de la photo: {photo_name} ({photo_path})")
        
        # Validate that it's actually an image file
        if not os.path.exists(photo_path):
            print(f"Erreur: Fichier {photo_path} n'existe pas")
            continue
            
        # Get file extension to determine format
        _, ext = os.path.splitext(photo_name.lower())
        if ext not in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff', '.webp']:
            print(f"Format non supporté: {ext}, conversion en PNG")
            # Try to load and convert with OpenCV
            try:
                img = cv2.imread(photo_path)
                if img is None:
                    print(f"Erreur: Impossible de lire l'image {photo_path}")
                    continue
                # Convert to PNG
                photo_filename = os.path.join(output_dir, f"photo_{i:04d}.png")
                cv2.imwrite(photo_filename, img)
            except Exception as e:
                print(f"Erreur lors de la conversion: {e}")
                continue
        else:
            # Copy the uploaded photo to temp_frames
            photo_filename = os.path.join(output_dir, f"photo_{i:04d}{ext}")
            try:
                shutil.copy2(photo_path, photo_filename)
            except Exception as e:
                print(f"Erreur lors de la copie: {e}")
                continue
        
        # Resize image if too large
        photo_filename = resize_image_if_needed(photo_filename)
        
        frame_paths.append(photo_filename)
        checkbox_choices.append((f"Photo {i+1} ({photo_name})", photo_filename))

    print(f"{len(frame_paths)} photos traitées avec succès sur {len(photo_files)} uploadées.")
    if len(frame_paths) < len(photo_files):
        print(f"⚠️ {len(photo_files) - len(frame_paths)} photos n'ont pas pu être traitées.")
    print(f"--- Fin du traitement des photos ---")
    
    all_extracted_frame_paths = frame_paths
    return frame_paths, gr.update(choices=checkbox_choices, value=[])

def update_checkbox_selection(evt: gr.SelectData, current_checkbox_values):
    """
    Updates the CheckboxGroup selection when a frame in the gallery is clicked.
    """
    global all_extracted_frame_paths # Declare global to access the list of all extracted frame paths

    if evt.index is not None and 0 <= evt.index < len(all_extracted_frame_paths):
        clicked_frame_path = all_extracted_frame_paths[evt.index]
        # The path from all_extracted_frame_paths is already normalized and correct
        if clicked_frame_path not in current_checkbox_values:
            current_checkbox_values.append(clicked_frame_path)
        else:
            current_checkbox_values.remove(clicked_frame_path) # Toggle selection
        return current_checkbox_values
    return current_checkbox_values # Return current values if no valid click

def validate_selection(selected_frames_list):
    """
    Validates the selection from the checkbox group and updates outputs.
    """
    debug_message = ""
    debug_message += f"Input selected_frames_list type: {type(selected_frames_list)}\n"
    debug_message += f"Input selected_frames_list: {selected_frames_list}\n"

    if selected_frames_list:
        debug_message += f"Frames validées: {', '.join(selected_frames_list)}\n"
        return ", ".join(selected_frames_list), debug_message
    debug_message += "Aucune frame sélectionnée à valider.\n"
    return "Aucune sélection", debug_message

def main():
    """
    Main function to launch the Gradio app.
    """
    with gr.Blocks() as demo:
        # State to hold the paths of the extracted frames
        frame_paths_state = gr.State([]) # Keep this for now, might be useful later

        gr.Markdown("# Module 1: Video Frame Extractor & Photo Analyzer")
        
        with gr.Tab("Video Frame Extractor & Photo Analyzer"):
            # Mode selector
            mode_selector = gr.Radio(
                label="Mode d'analyse",
                choices=["Vidéo", "Photos individuelles"],
                value="Vidéo"
            )
            
            with gr.Row():
                video_input = gr.Video(label="Vidéo", visible=True)
                photo_input = gr.File(
                    label="Photos individuelles", 
                    file_types=["image", ".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp", ".svg"], 
                    file_count="multiple",
                    visible=False
                )
            
            # Function to toggle visibility based on mode
            def toggle_mode(mode):
                if mode == "Vidéo":
                    return gr.update(visible=True), gr.update(visible=False)
                else:
                    return gr.update(visible=False), gr.update(visible=True)
            
            mode_selector.change(
                fn=toggle_mode,
                inputs=[mode_selector],
                outputs=[video_input, photo_input]
            )
            
            with gr.Row():
                interval_input = gr.Number(label="Intervalle d'extraction (en frames)", value=10, visible=True)
                extract_button = gr.Button("Extraire les frames", visible=True)
                process_photos_button = gr.Button("Traiter les photos", visible=False)
            
            # Function to toggle button visibility based on mode
            def toggle_buttons(mode):
                if mode == "Vidéo":
                    return gr.update(visible=True), gr.update(visible=True), gr.update(visible=False)
                else:
                    return gr.update(visible=False), gr.update(visible=False), gr.update(visible=True)
            
            mode_selector.change(
                fn=toggle_buttons,
                inputs=[mode_selector],
                outputs=[interval_input, extract_button, process_photos_button]
            )
            
            with gr.Row(): # New row for prompt selection
                prompt_dropdown = gr.Dropdown(
                    label="Sélectionner un prompt",
                    choices=prompt_choices,
                    value=default_prompt_value, # Default value from TOML
                    interactive=True
                )
                selected_prompt_output = gr.Textbox(label="Prompt sélectionné", interactive=False)

            with gr.Row(): # Main gallery and selection area
                with gr.Column(scale=2): # Main gallery takes more space
                    frame_gallery = gr.Gallery(label="Toutes les frames extraites", allow_preview=False, type="filepath") # No select=True
                
                with gr.Column(scale=1): # Output and validation area
                    # New CheckboxGroup for multi-selection
                    selected_frames_checkboxes = gr.CheckboxGroup(label="Sélectionner les frames à valider")
                    validate_button = gr.Button("Valider la sélection")

            with gr.Row(): # Final outputs
                selected_frame_path_output = gr.Textbox(label="Chemin(s) de la/des frame(s) sélectionnée(s)", interactive=False)
                debug_output = gr.Textbox(label="Debug Info", interactive=False, lines=5)

            # Connect the buttons to their functions
            extract_button.click(
                fn=extract_frames,
                inputs=[video_input, interval_input],
                outputs=[frame_gallery, selected_frames_checkboxes]
            )
            
            process_photos_button.click(
                fn=process_photos,
                inputs=[photo_input],
                outputs=[frame_gallery, selected_frames_checkboxes]
            )

            # Connect gallery selection to update the checkbox group
            frame_gallery.select(
                fn=update_checkbox_selection,
                inputs=[selected_frames_checkboxes], # Pass current checkbox values
                outputs=[selected_frames_checkboxes] # Update checkbox group
            )

            # Connect validate button to process the selected frames from checkbox group
            validate_button.click(
                fn=validate_selection,
                inputs=[selected_frames_checkboxes], # Input from CheckboxGroup
                outputs=[selected_frame_path_output, debug_output]
            )

        selected_frames_input_ollama, ollama_manual_prompt_textbox, ollama_prompt_dropdown = ollama_frame_analyzer_ui(prompt_choices_ollama=prompt_choices, initial_prompt=default_prompt_value)

        def update_ollama_input(selected_frames_str):
            return selected_frames_str

        selected_frame_path_output.change(
            fn=update_ollama_input,
            inputs=[selected_frame_path_output],
            outputs=[selected_frames_input_ollama]
        )

        prompt_dropdown.change(
            fn=lambda x: [x, x, x], # Update selected_prompt_output, ollama_manual_prompt_textbox, and ollama_prompt_dropdown
            inputs=[prompt_dropdown],
            outputs=[selected_prompt_output, ollama_manual_prompt_textbox, ollama_prompt_dropdown]
        )

    # Launch the app with debug mode for hot reloading
    demo.launch(debug=True)

if __name__ == "__main__":
    main()