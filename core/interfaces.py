from abc import ABC, abstractmethod
from typing import Dict, List, Any, Generator

class PromptLoader(ABC):
    """
    Interface pour charger la configuration et les prompts.
    Permet de changer la source (YAML, JSON, BDD, API) sans toucher à l'app.
    """
    @abstractmethod
    def load_config(self) -> tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Retourne un tuple (settings, prompts).
        """
        pass

class AIModel(ABC):
    """
    Interface pour les modèles d'IA (Gemini, GPT, Claude, Local).
    """
    @abstractmethod
    def analyze(self, images: List[Any], prompt: str, stream: bool = False) -> Generator[str, None, None] | str:
        """
        Analyse une ou plusieurs images avec un prompt.
        Doit supporter le streaming ou retourner une string complète.
        """
        pass

class ImageGenerator(ABC):
    """
    Interface pour la génération d'images (DALL-E, ComfyUI, Midjourney).
    """
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Génère une image à partir d'un prompt.
        Retourne le chemin local ou l'URL de l'image générée.
        """
        pass
