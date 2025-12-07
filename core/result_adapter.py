import re
import json
from typing import Dict, List, Tuple, Optional


class ResultAdapter:
    """
    Parses and structures raw Gemini output for UI consumption.
    Extracts JSON data and structured prompts from markdown-formatted responses.
    """
    
    def __init__(self):
        pass
    
    def parse_response(self, text: str, mode: str) -> Dict:
        """
        Main parsing method.
        
        Args:
            text: Raw text output from Gemini
            mode: Analysis mode (e.g., 'ultimate_biome_fashion_icon')
        
        Returns:
            {
                'prompts': [(title, content), ...],
                'json_data': {...} or None,
                'raw_text': str
            }
        """
        result = {
            'prompts': [],
            'json_data': None,
            'raw_text': text
        }
        
        # Extract JSON if applicable
        # Extract JSON if applicable
        # Expanded list to include all modes that produce JSON data
        json_modes = [
            "ultimate_biome_fashion_icon", 
            "fetish_mode_shorts", 
            "biome_ultra_detailed",
            "biometric_complete",
            "deepstack_biometrics",
            "experimental_fashion_lab",
            "alt_pov"
        ]
        
        if mode in json_modes:
            result['json_data'] = self._extract_json(text)
        
        # Extract structured prompts
        result['prompts'] = self._extract_prompts(text)
        
        return result
    
    def _extract_json(self, text: str) -> Optional[Dict]:
        """
        Extracts and validates JSON from markdown code blocks.
        
        Strategies:
        1. ```json ... ```
        2. ``` ... ``` (fallback)
        3. Raw { ... } (last resort)
        
        Returns:
            Parsed JSON dict or None if not found/invalid
        """
        json_str = None
        
        # Strategy 1: Look for ```json block
        match = re.search(r"```json\s*(.*?)\s*```", text, re.DOTALL)
        if match:
            json_str = match.group(1)
        else:
            # Strategy 2: Look for first ``` block (if model forgot 'json' tag)
            match = re.search(r"```\s*(.*?)\s*```", text, re.DOTALL)
            if match:
                candidate = match.group(1).strip()
                # Only accept if it starts with { (looks like JSON)
                if candidate.startswith('{'):
                    json_str = candidate
            
            if not json_str:
                # Strategy 3: Look for raw JSON structure { ... }
                match = re.search(r"\{.*\}", text, re.DOTALL)
                if match:
                    json_str = match.group(0)
        
        if json_str:
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                return None
        
        return None
    
    def _extract_prompts(self, text: str) -> List[Tuple[str, str]]:
        """
        Extracts structured prompts from text.
        
        Looks for sections with emoji headers (e.g., ## 💎 THE FASHION TRILOGY)
        followed by code blocks.
        
        Returns:
            List of (title, content) tuples
        """
        prompts = []
        
        # Extract all code blocks first
        code_blocks = re.findall(r'```(?:\w+)?\s*\n(.*?)\n\s*```', text, re.DOTALL)
        
        if not code_blocks:
            return prompts
        
        # Try to identify prompt types by looking for headers
        section_pattern = r'##\s*([🎯📸🧠🚀⚡💎🔥🔬][^#\n]+)\s*\n.*?```(?:\w+)?\s*\n(.*?)\n\s*```'
        matches = re.finditer(section_pattern, text, re.DOTALL)
        
        for match in matches:
            title = match.group(1).strip()
            content = match.group(2).strip()
            prompts.append((title, content))
        
        # Fallback: If no sections found, just number the blocks
        if not prompts:
            prompts = [(f"📝 Prompt {i+1}", block.strip()) for i, block in enumerate(code_blocks)]
        
        # Apply formatting to all extracted prompts
        formatted_prompts = []
        for title, content in prompts:
            formatted_content = self._format_prompt_multiline(content)
            formatted_prompts.append((title, formatted_content))
            
        return formatted_prompts

    def _format_prompt_multiline(self, text: str) -> str:
        """
        Automatically inserts newlines before section tags to ensure readability.
        Target tags: [SUBJECT], [LIGHTING], [STYLE], [POSE], etc.
        """
        # List of standard tags used in our prompts
        tags = [
            r"\[SUBJECT", r"\[MAIN SUBJECT", r"\[MODEL SPECS", 
            r"\[FASHION", r"\[FETISH FASHION", r"\[EXPERIMENTAL FASHION",
            r"\[POSE", r"\[POV", r"\[CONTEXT", 
            r"\[LIGHTING", r"\[VISUAL DETAILS", r"\[TECHNICAL",
            r"\[STYLE", r"\[AESTHETIC", r"\[ENVIRONMENT", r"\[TYPOGRAPHY",
            r"\[LOOK DESCRIPTION]"
        ]
        
        formatted_text = text
        
        for tag in tags:
            # Look for the tag preceded by something other than a newline (and not at start of string)
            # We replace it with \n\n[TAG...
            pattern = f"(?<!^)(?<!\\n)({tag})"
            formatted_text = re.sub(pattern, r"\n\n\1", formatted_text, flags=re.IGNORECASE)
            
            # Also handle cases where it's just a single newline, force double
            pattern_single = f"(?<!^)(?<!\\n)(\\n)({tag})"
            formatted_text = re.sub(pattern_single, r"\n\2", formatted_text, flags=re.IGNORECASE)

        return formatted_text
