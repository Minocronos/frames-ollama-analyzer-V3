import yaml
import os
from core.interfaces import PromptLoader
from typing import Dict, Any

class YamlPromptLoader(PromptLoader):
    """
    Charge les prompts depuis des fichiers YAML locaux.
    C'est l'implémentation par défaut pour le développement local.
    """
    def __init__(self, settings_path: str = "config/settings.yaml", prompts_path: str = "config/prompts.yaml"):
        self.settings_path = settings_path
        self.prompts_path = prompts_path

    def load_config(self) -> tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Lit les fichiers YAML et retourne les dictionnaires.
        """
        if not os.path.exists(self.settings_path):
            raise FileNotFoundError(f"Settings file not found: {self.settings_path}")
        
        if not os.path.exists(self.prompts_path):
            raise FileNotFoundError(f"Prompts file not found: {self.prompts_path}")

        with open(self.settings_path, "r", encoding="utf-8") as f:
            settings = yaml.safe_load(f)
        
        with open(self.prompts_path, "r", encoding="utf-8") as f:
            prompts = yaml.safe_load(f)
            
        return settings, prompts
