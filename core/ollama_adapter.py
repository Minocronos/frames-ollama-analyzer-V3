import ollama
from PIL import Image
import io
from core.interfaces import AIModel

class OllamaAdapter(AIModel):
    """
    Adaptateur pour Ollama (local ou cloud).
    Supporte tous les modèles disponibles via Ollama (Llama, Mistral, Gemini, etc.)
    """
    def __init__(self, model_name="gemini-3-pro-preview", temperature=0.7):
        self.model_name = model_name
        self.temperature = temperature

    def analyze(self, frames, prompt, stream=True):
        """
        Send frames and prompt to AI model via Ollama.
        
        Args:
            frames (list): List of PIL Image objects.
            prompt (str): The text prompt.
            stream (bool): Whether to stream the response.
            
        Yields:
            str: Chunks of the response if streaming.
        """
        # Convert PIL images to bytes for Ollama
        images_bytes = []
        for frame in frames:
            # Handle RGBA/Transparency by converting to RGB with white background
            if frame.mode in ('RGBA', 'LA') or (frame.mode == 'P' and 'transparency' in frame.info):
                background = Image.new('RGB', frame.size, (255, 255, 255))
                if frame.mode == 'P':
                    frame = frame.convert('RGBA')
                background.paste(frame, mask=frame.split()[-1])
                frame = background
            elif frame.mode != 'RGB':
                frame = frame.convert('RGB')
                
            img_byte_arr = io.BytesIO()
            frame.save(img_byte_arr, format='JPEG')
            images_bytes.append(img_byte_arr.getvalue())

        # Call Ollama
        # Note: Ollama python client handles image bytes directly in 'images' list
        try:
            response = ollama.generate(
                model=self.model_name,
                prompt=prompt,
                images=images_bytes,
                stream=stream,
                options={
                    "temperature": self.temperature
                }
            )
        except Exception as e:
            if "temperature" in str(e).lower() and self.temperature > 2.0:
                print(f"⚠️ Temperature {self.temperature} rejected by model. Falling back to 2.0.")
                response = ollama.generate(
                    model=self.model_name,
                    prompt=prompt,
                    images=images_bytes,
                    stream=stream,
                    options={
                        "temperature": 2.0
                    }
                )
            else:
                raise e
        
        if stream:
            for chunk in response:
                yield chunk['response']
        else:
            return response['response']
