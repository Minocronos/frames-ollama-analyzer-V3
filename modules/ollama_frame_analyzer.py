# modules/ollama_frame_analyzer.py

import gradio as gr
import os
import ollama
from PIL import Image
import io
import base64
import toml
import time

PROMPTS_DIR = '../prompts/'

def encode_image(image_path):
    """Encode image from path to base64"""
    try:
        with Image.open(image_path) as img:
            buffered = io.BytesIO()
            img.save(buffered, format="PNG")
            return base64.b64encode(buffered.getvalue()).decode("utf-8")
    except Exception as e:
        print(f"Error encoding image {image_path}: {e}")
        return None

def get_prompt_files():
    if not os.path.exists(PROMPTS_DIR):
        return []
    return [f for f in os.listdir(PROMPTS_DIR) if f.endswith('.toml')]

def read_prompt_file(filename):
    with open(os.path.join(PROMPTS_DIR, filename), 'r', encoding='utf-8') as f:
        return toml.load(f)

# Default Ollama URL (can be overridden for cloud)
OLLAMA_URL = "http://localhost:11434"

def get_ollama_url(mode):
    if "Local" in mode:
        return "http://localhost:11434"
    else:
        return "https://ollama.com"

def list_ollama_models(ollama_url, api_key=None):
    try:
        headers = {'Authorization': f'Bearer {api_key}'} if api_key else {}
        client = ollama.Client(host=ollama_url, headers=headers)
        response = client.list()

        models_out = []

        # Response can be several types (ListResponse, dict, list). Normalize it.
        if hasattr(response, 'models'):
            # e.g. ollama._types.ListResponse
            candidates = getattr(response, 'models') or []
        elif isinstance(response, dict):
            # Common shape: {'models': [ {...}, ... ]}
            candidates = response.get('models') or response.get('tags') or []
        elif isinstance(response, list):
            candidates = response
        else:
            candidates = []

        for item in candidates:
            # item may be a string (model name) or a dict with keys like 'name', 'model', 'id'
            if isinstance(item, str):
                models_out.append(item)
            elif isinstance(item, dict):
                for key in ('name', 'model', 'id'):
                    if key in item:
                        models_out.append(item[key])
                        break
                else:
                    # Fallback: try common nested shapes or stringify
                    # e.g. {'model': {'name': 'xyz'}}
                    if 'model' in item and isinstance(item['model'], dict) and 'name' in item['model']:
                        models_out.append(item['model']['name'])
                    else:
                        models_out.append(str(item))
            else:
                # Try attribute access for custom types (e.g. ollama._types.Model)
                for attr in ('name', 'model', 'id'):
                    val = getattr(item, attr, None)
                    if val:
                        models_out.append(val)
                        break
                else:
                    models_out.append(str(item))

        return models_out
    except Exception as e:
        # Print exception for debugging but do not crash the UI
        print(f"Error listing Ollama models: {e}")
        return []

def call_ollama_with_retry(client, model_name, messages, max_retries=2, delay=1):
    """Call Ollama API with retry logic for temporary errors"""
    for attempt in range(max_retries + 1):
        try:
            return client.chat(
                model=model_name,
                messages=messages,
                stream=False
            )
        except Exception as e:
            if attempt < max_retries and "Internal Server Error" in str(e):
                print(f"DEBUG: Attempt {attempt + 1} failed with Internal Server Error, retrying in {delay}s...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                # Instead of raising, return an error object so the caller can handle it gracefully
                print(f"DEBUG: call_ollama_with_retry final failure: {e}")
                return {'error': str(e)}

def analyze_frame_with_ollama(selected_frames_str, model_name, analysis_prompt, analysis_options, mode, api_key=None):
    ollama_url = get_ollama_url(mode)
    if not selected_frames_str:
        return "No frames selected for analysis.", ""
    if not model_name:
        return "Please select an Ollama model.", ""
    if not analysis_prompt:
        return "Please provide an analysis prompt.", ""

    selected_frames = [path.strip() for path in selected_frames_str.split(',') if path.strip()]

    results = []
    client = ollama.Client(host=ollama_url, headers={'Authorization': f'Bearer {api_key}'} if api_key else {})

    # Initialize full_prompt to avoid UnboundLocalError
    full_prompt = analysis_prompt

    # Check if this is a multi-image analysis (multiple frames that should be analyzed together)
    progression_keywords = ["progression", "transformation", "evolution", "sequence", "chronologically", "transition", "comparison", "before", "after"]
    is_multi_image_analysis = (any(keyword in analysis_prompt.lower() for keyword in progression_keywords) and len(selected_frames) > 1) or len(selected_frames) > 1

    if is_multi_image_analysis:
        # For multi-image analysis, first analyze each image separately if there's a manual prompt
        individual_analyses = []
        if analysis_prompt and analysis_prompt.strip():
            # Analyze each image individually first
            for frame_path in selected_frames:
                try:
                    image_base64 = encode_image(frame_path)
                    if image_base64 is None:
                        individual_analyses.append(f"Error: Could not encode image {os.path.basename(frame_path)}")
                        continue

                    full_individual_prompt = analysis_prompt
                    if analysis_options:
                        full_individual_prompt += f" Analyze for: {', '.join(analysis_options)}."
                    
                    response = call_ollama_with_retry(
                        client,
                        model_name,
                        messages=[
                            {
                                "role": "user",
                                "content": full_individual_prompt,
                                "images": [image_base64]
                            }
                        ]
                    )
                    
                    # Normalize response and handle errors
                    if isinstance(response, dict) and 'error' in response:
                        individual_analyses.append(f"--- Analysis for {os.path.basename(frame_path)} ---\nError: {response['error']}")
                    else:
                        content = None
                        if isinstance(response, dict) and 'message' in response and isinstance(response['message'], dict) and 'content' in response['message']:
                            content = response['message']['content']
                        else:
                            msg = getattr(response, 'message', None)
                            if isinstance(msg, dict) and 'content' in msg:
                                content = msg['content']
                            elif hasattr(msg, 'content'):
                                content = getattr(msg, 'content')

                        if content is None:
                            individual_analyses.append(f"--- Analysis for {os.path.basename(frame_path)} ---\nError: unexpected response format: {str(response)}")
                        else:
                            individual_analyses.append(f"--- Analysis for {os.path.basename(frame_path)} ---\n" + content)
                    
                except Exception as e:
                    error_msg = f"Error analyzing {os.path.basename(frame_path)}: {e}"
                    print(f"DEBUG: {error_msg}")  # Debug logging
                    individual_analyses.append(error_msg)
            
            results.extend(individual_analyses)
        
        # Now create the mix prompt
        try:
            images_base64 = []
            for frame_path in selected_frames:
                image_base64 = encode_image(frame_path)
                if image_base64 is None:
                    continue
                images_base64.append(image_base64)

            if not images_base64:
                return "Error: Could not encode any images.", ""

            # Create mix prompt that incorporates the user's manual prompt if provided
            mix_instruction = f"J'ai uploadé {len(images_base64)} images pour analyse."
            if individual_analyses:
                mix_instruction += " Voici les analyses individuelles :\n" + "\n\n".join(individual_analyses)
            mix_instruction += " D'abord, fournis une analyse claire et structurée : décris chaque image individuellement en détail, puis fais une comparaison objective entre elles. Ensuite, crée un prompt détaillé pour générer une NOUVELLE image composite originale qui mélange artistiquement ces éléments."
            if analysis_prompt and analysis_prompt.strip():
                mix_instruction += f" Intègre ces instructions spécifiques dans le prompt de génération : '{analysis_prompt}'"
            mix_instruction += " C'est un travail artistique d'expérimentations créatives - les mélanges sont purement artistiques. Fournis le prompt final de manière claire et utilisable."
            
            if analysis_options:
                mix_instruction += f" Analyse pour: {', '.join(analysis_options)}."
            
            if analysis_options:
                mix_instruction += f" Analyse pour: {', '.join(analysis_options)}."
            
            response = call_ollama_with_retry(
                client,
                model_name,
                messages=[
                    {
                        "role": "user",
                        "content": mix_instruction,
                        "images": images_base64
                    }
                ]
            )
            
            # Normalize mix response and handle errors
            if isinstance(response, dict) and 'error' in response:
                results.append(f"--- Mix Prompt Generation ---\nError: {response['error']}")
            else:
                mix_content = None
                if isinstance(response, dict) and 'message' in response and isinstance(response['message'], dict) and 'content' in response['message']:
                    mix_content = response['message']['content']
                else:
                    mmsg = getattr(response, 'message', None)
                    if isinstance(mmsg, dict) and 'content' in mmsg:
                        mix_content = mmsg['content']
                    elif hasattr(mmsg, 'content'):
                        mix_content = getattr(mmsg, 'content')

                if mix_content is None:
                    results.append(f"--- Mix Prompt Generation ---\nError: unexpected response format: {str(response)}")
                else:
                    results.append("--- Mix Prompt Generation ---\n" + mix_content)
            
        except Exception as e:
            error_msg = f"Error in mix prompt generation: {e}"
            print(f"DEBUG: Mix prompt generation failed: {error_msg}")  # Debug logging
            results.append(error_msg)
            
        except Exception as e:
            results.append(f"Error analyzing images: {e}")
    else:
        # Analyze each frame individually
        for frame_path in selected_frames:
            try:
                image_base64 = encode_image(frame_path)
                if image_base64 is None:
                    results.append(f"Error: Could not encode image {os.path.basename(frame_path)}")
                    continue

                full_prompt = analysis_prompt
                if analysis_options:
                    full_prompt += f" Analyze for: {', '.join(analysis_options)}."
                
                response = call_ollama_with_retry(
                    client,
                    model_name,
                    messages=[
                        {
                            "role": "user",
                            "content": full_prompt,
                            "images": [image_base64]
                        }
                    ]
                )
                
                # Normalize response and handle errors
                if isinstance(response, dict) and 'error' in response:
                    results.append(f"--- Analysis for {os.path.basename(frame_path)} ---\nError: {response['error']}")
                else:
                    content = None
                    if isinstance(response, dict) and 'message' in response and isinstance(response['message'], dict) and 'content' in response['message']:
                        content = response['message']['content']
                    else:
                        msg = getattr(response, 'message', None)
                        if isinstance(msg, dict) and 'content' in msg:
                            content = msg['content']
                        elif hasattr(msg, 'content'):
                            content = getattr(msg, 'content')

                    if content is None:
                        results.append(f"--- Analysis for {os.path.basename(frame_path)} ---\nError: unexpected response format: {str(response)}")
                    else:
                        results.append(f"--- Analysis for {os.path.basename(frame_path)} ---\n" + content)
                
            except Exception as e:
                results.append(f"Error analyzing {os.path.basename(frame_path)}: {e}")
    
    return "\n\n".join(results), full_prompt
def update_constructed_prompt(analysis_prompt, analysis_options):
    full_prompt = analysis_prompt if analysis_prompt else ""
    if analysis_options:
        full_prompt += f" Analyze for: {', '.join(analysis_options)}."
    return full_prompt

def ollama_frame_analyzer_ui(prompt_choices_ollama: list, initial_prompt: str = ""):
    with gr.Tab("Ollama Frame Analyzer"):
        gr.Markdown("## Analyze Frames with Ollama")
        
        with gr.Row():
            with gr.Column():
                selected_frames_input = gr.Textbox(label="Selected Frames (from previous module)", interactive=False)

                # New fields for Ollama configuration
                ollama_mode_input = gr.Dropdown(
                    label="Ollama Mode",
                    choices=["Local (http://localhost:11434)", "Cloud (https://ollama.com)"],
                    value="Local (http://localhost:11434)",
                    interactive=True
                )
                api_key_input = gr.Textbox(label="API Key (for cloud models)", type="password", interactive=True)

                # Get initial models based on default mode
                initial_mode = "Local (http://localhost:11434)"
                initial_url = get_ollama_url(initial_mode)
                available_models = list_ollama_models(initial_url)
                
                # Choose default model for initial mode
                default_model = None
                if available_models:
                    if "Cloud" in initial_mode:
                        preferred_cloud = ['qwen3-vl:235b', 'qwen3vl', 'qwen3-vl', 'deepseek-v3.1:671b-cloud']
                        for pref in preferred_cloud:
                            if any(pref.lower() in model.lower() for model in available_models):
                                default_model = next((m for m in available_models if pref.lower() in m.lower()), None)
                                if default_model:
                                    break
                        if not default_model:
                            vision_models = [m for m in available_models if 'vl' in m.lower() or 'vision' in m.lower() or 'qwen3' in m.lower()]
                            if vision_models:
                                default_model = vision_models[0]
                            else:
                                default_model = available_models[0]
                    else:
                        # For local mode, prefer specific vision models
                        preferred_local = ['qwen2.5-vl:7b', 'qwen2.5vl', 'llava', 'bakllava']
                        for pref in preferred_local:
                            if any(pref.lower() in model.lower() for model in available_models):
                                default_model = next((m for m in available_models if pref.lower() in m.lower()), None)
                                if default_model:
                                    break
                        if not default_model:
                            default_model = available_models[0]
                
                ollama_model_dropdown = gr.Dropdown(
                    label="Select Ollama Model",
                    choices=available_models,
                    value=default_model,
                    interactive=True
                )

                ollama_prompt_dropdown = gr.Dropdown(
                    label="Select Analysis Prompt",
                    choices=["", *prompt_choices_ollama],
                    value="",
                    interactive=True
                )

                manual_prompt_textbox = gr.Textbox(
                    label="Analysis Prompt (e.g., 'Describe the image')",
                    value=initial_prompt,
                    lines=5,
                    interactive=True
                )
                options_checkbox_group = gr.CheckboxGroup(
                    label="Specific Analysis Focus",
                    choices=["people", "clothes", "pose", "action", "attitudes", "faces", "bodies"],
                    value=[], # No pre-selected options by default
                    interactive=True
                )
                analyze_button = gr.Button("Analyze Selected Frames")

            with gr.Column():
                analysis_results_output = gr.Textbox(label="Analysis Results", interactive=False, lines=10)
                constructed_prompt_output = gr.Textbox(label="Constructed Prompt (sent to LLM)", interactive=False, lines=5)

        # Function to update models list
        def update_models(mode, api_key):
            url = get_ollama_url(mode)
            models = list_ollama_models(url, api_key)
            
            # Choose default model based on mode
            default_model = None
            if models:
                if "Cloud" in mode:
                    # For cloud mode, prefer specific vision models
                    preferred_cloud = ['qwen3-vl:235b', 'qwen3vl', 'qwen3-vl', 'deepseek-v3.1:671b-cloud']
                    for pref in preferred_cloud:
                        if any(pref.lower() in model.lower() for model in models):
                            default_model = next((m for m in models if pref.lower() in m.lower()), None)
                            if default_model:
                                break
                    if not default_model:
                        # Fallback to any vision-capable model
                        vision_models = [m for m in models if 'vl' in m.lower() or 'vision' in m.lower() or 'qwen3' in m.lower()]
                        if vision_models:
                            default_model = vision_models[0]
                        else:
                            default_model = models[0]
                else:
                    # For local mode, prefer specific vision models
                    preferred_local = ['qwen2.5-vl:7b', 'qwen2.5vl', 'llava', 'bakllava']
                    for pref in preferred_local:
                        if any(pref.lower() in model.lower() for model in models):
                            default_model = next((m for m in models if pref.lower() in m.lower()), None)
                            if default_model:
                                break
                    if not default_model:
                        default_model = models[0]
            
            return gr.update(choices=models, value=default_model)

        # Event handlers
        ollama_mode_input.change(
            fn=update_models,
            inputs=[ollama_mode_input, api_key_input],
            outputs=[ollama_model_dropdown]
        )

        api_key_input.change(
            fn=update_models,
            inputs=[ollama_mode_input, api_key_input],
            outputs=[ollama_model_dropdown]
        )

        ollama_prompt_dropdown.change(
            fn=lambda x: x,
            inputs=[ollama_prompt_dropdown],
            outputs=[manual_prompt_textbox]
        )

        # Real-time update for constructed_prompt_output
        ollama_prompt_dropdown.change(
            fn=update_constructed_prompt,
            inputs=[manual_prompt_textbox, options_checkbox_group],
            outputs=[constructed_prompt_output]
        )

        options_checkbox_group.change(
            fn=update_constructed_prompt,
            inputs=[manual_prompt_textbox, options_checkbox_group],
            outputs=[constructed_prompt_output]
        )

        manual_prompt_textbox.change(
            fn=update_constructed_prompt,
            inputs=[manual_prompt_textbox, options_checkbox_group],
            outputs=[constructed_prompt_output]
        )

        analyze_button.click(
            fn=analyze_frame_with_ollama,
            inputs=[selected_frames_input, ollama_model_dropdown, manual_prompt_textbox, options_checkbox_group, ollama_mode_input, api_key_input],
            outputs=[analysis_results_output, constructed_prompt_output]
        )
    return selected_frames_input, manual_prompt_textbox, ollama_prompt_dropdown