import cv2
from PIL import Image
import tempfile
import os

class VideoProcessor:
    def __init__(self, extraction_interval=2):
        """
        Args:
            extraction_interval (int): Extract 1 frame every N seconds.
        """
        self.extraction_interval = extraction_interval

    def process_video(self, video_file, strategy="interval", value=2):
        """
        Process a video file and extract frames.
        
        Args:
            video_file: Streamlit UploadedFile.
            strategy (str): "interval" (seconds) or "count" (total frames).
            value (int): The interval in seconds OR the total number of frames.
        
        Returns:
            list: List of PIL Image objects.
        """
        # Save uploaded file to temp file because cv2 needs a path
        tfile = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        tfile.write(video_file.read())
        tfile.close()
        
        frames = []
        cap = cv2.VideoCapture(tfile.name)
        
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0
        
        if fps == 0:
            fps = 30 # Fallback
            
        # Calculate Frame Interval
        if strategy == "count":
            target_count = max(1, int(value))
            if total_frames > 0:
                frame_interval = max(1, int(total_frames / target_count))
            else:
                frame_interval = int(fps) # Fallback
        else: # strategy == "interval"
            interval_sec = max(0.1, float(value))
            frame_interval = max(1, int(fps * interval_sec))
        
        count = 0
        extracted_count = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
                
            if count % frame_interval == 0:
                # Convert BGR to RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(rgb_frame)
                frames.append(pil_image)
                extracted_count += 1
                
                # Stop if we hit the target count (only for count strategy to be precise)
                if strategy == "count" and extracted_count >= value:
                    break
            
            count += 1
            
        cap.release()
        os.unlink(tfile.name) # Clean up temp file
        
        return frames
